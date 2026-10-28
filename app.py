import streamlit as st
import streamlit.components.v1 as components
import os
import io
import re
import base64
import zipfile
import tempfile
import subprocess
import urllib.request
from lxml import etree
import pdfkit
from PyPDF2 import PdfMerger

# --- YOL AYARLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = tempfile.gettempdir()
WK_DIR = os.path.join(TEMP_DIR, "wkhtmltox")
WK_PATH = os.path.join(WK_DIR, "bin", "wkhtmltopdf")

# --- LINUX İÇİN PDF MOTORUNU TEMP KLASÖRÜNE KURMA ---
@st.cache_resource
def motoru_indir():
    if not os.path.exists(WK_PATH):
        tar_yolu = os.path.join(TEMP_DIR, "wk.tar.xz")
        urllib.request.urlretrieve("https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz", tar_yolu)
        subprocess.run(["tar", "xf", tar_yolu, "-C", TEMP_DIR], check=True)
        subprocess.run(["chmod", "+x", WK_PATH], check=True)

try:
    motoru_indir()
except Exception as e:
    pass

st.set_page_config(page_title="E-Fatura Toplu PDF Dönüştürücü", page_icon="📄", layout="centered")

def tum_arsivleri_ac(klasor_yolu):
    bulundu = True
    while bulundu:
        bulundu = False
        for root_dir, dirs, files in os.walk(klasor_yolu):
            for file in files:
                dosya_yolu = os.path.join(root_dir, file)
                if file.lower().endswith('.zip'):
                    if zipfile.is_zipfile(dosya_yolu):
                        try:
                            with zipfile.ZipFile(dosya_yolu, 'r') as zip_ref:
                                zip_ref.extractall(root_dir)
                            os.remove(dosya_yolu)
                            bulundu = True
                        except Exception: pass

def faturanin_tarihini_bul(xml_path):
    try:
        with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
            icerik = f.read()
        tarih_match = re.search(r'<cbc:IssueDate>([^<]+)</cbc:IssueDate>', icerik)
        saat_match = re.search(r'<cbc:IssueTime>([^<]+)</cbc:IssueTime>', icerik)
        tarih = tarih_match.group(1).strip() if tarih_match else "9999-99-99"
        saat = saat_match.group(1).strip() if saat_match else "00:00:00"
        return f"{tarih} {saat}"
    except Exception:
        return "9999-99-99 00:00:00"

def xml_to_pdf(xml_path, output_pdf_path, fallback_xslt_path=None, bim_xslt_path=None):
    try:
        with open(xml_path, 'rb') as f:
            raw_content = f.read()
            
        if raw_content.startswith(b'\xef\xbb\xbf'):
            raw_content = raw_content[3:]
            
        is_bim = b'1750051846' in raw_content or b'earsivbimxslt' in raw_content
            
        raw_content = re.sub(br'<\?xml-stylesheet[^>]*\?>', b'', raw_content)
        
        esnek_parser = etree.XMLParser(recover=True, no_network=True, resolve_entities=False)
        tree = etree.fromstring(raw_content, parser=esnek_parser)
        
        xslt_content = None
        namespaces = {
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        }

        for obj in tree.findall('.//cbc:EmbeddedDocumentBinaryObject', namespaces):
            if not obj.text: continue
            try:
                decoded = base64.b64decode(obj.text.strip(), validate=False)
                if decoded.startswith(b'PK\x03\x04'):
                    mem_zip = io.BytesIO(decoded)
                    if zipfile.is_zipfile(mem_zip):
                        with zipfile.ZipFile(mem_zip) as z:
                            for name in z.namelist():
                                content = z.read(name)
                                if b'<xsl:stylesheet' in content or b'<xsl:transform' in content:
                                    xslt_content = content
                                    break
                elif b'<xsl:stylesheet' in decoded or b'<xsl:transform' in decoded:
                    xslt_content = decoded
                if xslt_content: break
            except Exception: pass

        if not xslt_content:
            for elem in tree.iter():
                if elem.text and len(elem.text.strip()) > 100:
                    metin = elem.text.strip()
                    if '<xsl:stylesheet' in metin or '<xsl:transform' in metin:
                        xslt_content = metin.encode('utf-8')
                        break
                    try:
                        decoded = base64.b64decode(metin, validate=False)
                        if decoded.startswith(b'PK\x03\x04'):
                            mem_zip = io.BytesIO(decoded)
                            if zipfile.is_zipfile(mem_zip):
                                with zipfile.ZipFile(mem_zip) as z:
                                    for name in z.namelist():
                                        content = z.read(name)
                                        if b'<xsl:stylesheet' in content or b'<xsl:transform' in content:
                                            xslt_content = content
                                            break
                        elif b'<xsl:stylesheet' in decoded or b'<xsl:transform' in decoded:
                            xslt_content = decoded
                    except Exception: pass
                    if xslt_content: break

        if not xslt_content and is_bim and bim_xslt_path and os.path.exists(bim_xslt_path):
            with open(bim_xslt_path, 'rb') as f_bim:
                xslt_content = f_bim.read()

        transform = None
        hata_mesaji = ""
        
        # --- ŞABLON DERLEME VE DIŞ BAĞLANTI TEMİZLEYİCİ ---
        def sablon_derle(content_bytes):
            xslt_str = content_bytes.decode('utf-8', errors='ignore')
            xslt_str = re.sub(r'<\?xml.*\?>', '', xslt_str)
            xslt_str = re.sub(r'<xsl:(import|include)[^>]*href=["\']http[^"\']+["\'][^>]*?/?>', '', xslt_str, flags=re.IGNORECASE)
            xslt_root = etree.fromstring(xslt_str.encode('utf-8'), parser=esnek_parser)
            return etree.XSLT(xslt_root)

        if xslt_content:
            try:
                transform = sablon_derle(xslt_content)
            except Exception as e:
                hata_mesaji += f"Orijinal Şablon Hatası: {str(e)} | "
                transform = None 

        if transform is None and fallback_xslt_path and os.path.exists(fallback_xslt_path):
            try:
                with open(fallback_xslt_path, 'rb') as f_sablon:
                    fallback_content = f_sablon.read()
                transform = sablon_derle(fallback_content)
            except Exception as e:
                hata_mesaji += f"Yedek Şablon Hatası: {str(e)}"
                transform = None
                
        if transform is None:
            return False, f"Hiçbir şablon uygulanamadı. {hata_mesaji}"

        html_dom = transform(tree)
        
        config = pdfkit.configuration(wkhtmltopdf=WK_PATH)
        options = {
            'page-size': 'A4', 
            'encoding': "UTF-8", 
            'enable-local-file-access': "",
            'enable-javascript': "",
            'javascript-delay': 1000,
            'no-outline': None, 
            'quiet': ''
        }
        pdfkit.from_string(str(html_dom), output_pdf_path, configuration=config, options=options)
        
        if not os.path.exists(output_pdf_path) or os.path.getsize(output_pdf_path) < 10:
            return False, "PDF dosyası fiziksel olarak oluşturulamadı."
            
        return True, ""
    except Exception as e:
        return False, f"Teknik Hata: {str(e)}"

# ----- WEB ARAYÜZÜ -----
st.title("🚀 E-Fatura Toplu PDF Dönüştürücü")
st.markdown("XML faturalarınızı veya faturaları içeren ZIP arşivlerini buraya yükleyin. Sistem hepsini **tarih sırasına göre** tek bir PDF olarak size sunacaktır.")

uploaded_files = st.file_uploader("XML veya ZIP Dosyalarını Seçin", accept_multiple_files=True, type=['xml', 'zip'])

if st.button("Faturaları Birleştir ve PDF Yap", type="primary"):
    if not uploaded_files:
        st.warning("Lütfen en az bir dosya yükleyin.")
    else:
        with st.spinner('Motor hazırlanıyor ve faturalar işleniyor, lütfen bekleyin...'):
            with tempfile.TemporaryDirectory() as work_dir:
                xml_dosyalari = []
                
                for uploaded_file in uploaded_files:
                    hedef_yol = os.path.join(work_dir, uploaded_file.name)
                    with open(hedef_yol, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                tum_arsivleri_ac(work_dir)

                for root, _, files in os.walk(work_dir):
                    for file in files:
                        tam_yol = os.path.join(root, file)
                        if file.lower().endswith('.xml'):
                            if tam_yol not in xml_dosyalari:
                                xml_dosyalari.append(tam_yol)
                        elif not file.lower().endswith(('.pdf', '.html', '.htm', '.xslt', '.png', '.jpg')):
                            try:
                                with open(tam_yol, 'rb') as tf:
                                    head = tf.read(250)
                                    if b'<?xml' in head or b'<Invoice' in head:
                                        if tam_yol not in xml_dosyalari:
                                            xml_dosyalari.append(tam_yol)
                            except: pass

                if not xml_dosyalari:
                    st.error("Yüklenen dosyaların içinde geçerli bir XML bulunamadı.")
                else:
                    xml_dosyalari.sort(key=lambda x: faturanin_tarihini_bul(x))
                    
                    merger = PdfMerger()
                    basarili_sayisi = 0
                    basarisiz_sayisi = 0
                    hata_loglari = []
                    
                    varsayilan_sablon = os.path.join(BASE_DIR, "sablon.xslt")
                    bim_sablon = os.path.join(BASE_DIR, "bim_sablon.xslt")
                    
                    for idx, xml_yol in enumerate(xml_dosyalari):
                        pdf_cikti = os.path.join(work_dir, f"fatura_{idx}.pdf")
                        basarili_mi, hata_mesaji = xml_to_pdf(xml_yol, pdf_cikti, fallback_xslt_path=varsayilan_sablon, bim_xslt_path=bim_sablon)
                        
                        if basarili_mi:
                            merger.append(pdf_cikti)
                            basarili_sayisi += 1
                        else:
                            basarisiz_sayisi += 1
                            hata_loglari.append(f"Fatura ({os.path.basename(xml_yol)}): {hata_mesaji}")
                            
                    if basarili_sayisi > 0:
                        final_pdf_yolu = os.path.join(work_dir, "BIRLESTIRILMIS_FATURALAR.pdf")
                        merger.write(final_pdf_yolu)
                        merger.close()
                        
                        st.success(f"✅ İşlem Tamamlandı! {basarili_sayisi} adet fatura tarih sırasına göre birleştirildi.")
                        
                        if basarisiz_sayisi > 0:
                            st.info(f"Not: {basarisiz_sayisi} adet fatura sorunlu olduğu için atlandı.")
                            with st.expander("Hata Detaylarını Görmek İçin Tıklayın"):
                                for log in hata_loglari:
                                    st.write(log)
                            
                        with open(final_pdf_yolu, "rb") as pdf_file:
                            PDFbyte = pdf_file.read()
                        
                        b64 = base64.b64encode(PDFbyte).decode()
                        js_kodu = f"""
                        <script>
                            var a = document.createElement('a');
                            a.href = 'data:application/pdf;base64,{b64}';
                            a.download = 'BIRLESTIRILMIS_FATURALAR.pdf';
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        </script>
                        """
                        components.html(js_kodu, height=0)
                        
                        st.download_button(
                            label="📥 İndirme Başlamadıysa Buraya Tıklayın",
                            data=PDFbyte,
                            file_name="BIRLESTIRILMIS_FATURALAR.pdf",
                            mime="application/octet-stream"
                        )
                    else:
                        st.error("Hiçbir fatura dönüştürülemedi. Lütfen aşağıdaki hata raporunu bana kopyalayıp gönderin:")
                        for log in hata_loglari:
                            st.error(log)

st.markdown("---")
st.caption("Güvenlik Notu: Yüklenen tüm faturalar ve oluşturulan PDF'ler, işlem biter bitmez sunucudan kalıcı olarak silinir.")
