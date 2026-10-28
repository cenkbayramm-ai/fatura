import streamlit as st
import os
import io
import re
import shutil
import base64
import zipfile
import tempfile
import subprocess
from lxml import etree
import pdfkit
from PyPDF2 import PdfMerger

# --- LINUX İÇİN PDF MOTORUNU OTOMATİK KURMA SİSTEMİ ---
WK_DIR = os.path.join(os.getcwd(), "wkhtmltox")
WK_PATH = os.path.join(WK_DIR, "bin", "wkhtmltopdf")

if not os.path.exists(WK_PATH):
    try:
        subprocess.run(["wget", "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz"], check=True)
        subprocess.run(["tar", "xvf", "wkhtmltox-0.12.4_linux-generic-amd64.tar.xz"], check=True)
        subprocess.run(["chmod", "+x", WK_PATH], check=True)
    except Exception as e:
        print("Motor indirme hatası:", e)
# ------------------------------------------------------

st.set_page_config(page_title="E-Fatura PDF Çevirici", page_icon="📄", layout="centered")

def tum_arsivleri_ac(klasor_yolu):
    # İç içe geçmiş tüm ZIP'leri ve klasörleri en derine kadar çıkarır
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

def xml_to_pdf(xml_path, output_pdf_path, fallback_xslt_path=None):
    try:
        with open(xml_path, 'rb') as f:
            raw_content = f.read()
            
        if raw_content.startswith(b'\xef\xbb\xbf'):
            raw_content = raw_content[3:]
            
        raw_content = re.sub(br'(xmlns|xsi):schemaLocation\s*=\s*["\'][^"\']*["\']', b'', raw_content)
        
        esnek_parser = etree.XMLParser(recover=True)
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

        if not xslt_content and fallback_xslt_path and os.path.exists(fallback_xslt_path):
            with open(fallback_xslt_path, 'rb') as f_sablon:
                xslt_content = f_sablon.read()

        if not xslt_content:
            return False

        xslt_content_str = xslt_content.decode('utf-8', errors='ignore')
        xslt_content_str = re.sub(r'<\?xml.*\?>', '', xslt_content_str)
        xslt_content_str = re.sub(r'/\.(cac|cbc|ext|ds|xades|ubl)', r'./\1', xslt_content_str)
        xslt_content_str = xslt_content_str.replace('="/.', '="./').replace("='/.", "='./")

        xslt_root = etree.fromstring(xslt_content_str.encode('utf-8'), parser=esnek_parser)
        transform = etree.XSLT(xslt_root)
        html_dom = transform(tree)
        
        config = pdfkit.configuration(wkhtmltopdf=WK_PATH)
        options = {'page-size': 'A4', 'encoding': "UTF-8", 'no-outline': None, 'quiet': ''}
        pdfkit.from_string(str(html_dom), output_pdf_path, configuration=config, options=options)
        
        return os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 10
    except Exception:
        return False

# ----- WEB ARAYÜZÜ -----
st.title("🚀 E-Fatura Toplu PDF Dönüştürücü")
st.markdown("XML faturalarınızı veya faturaları içeren ZIP arşivlerini buraya yükleyin. Sistem hepsini tek bir PDF olarak size sunacaktır.")

uploaded_files = st.file_uploader("XML veya ZIP Dosyalarını Seçin", accept_multiple_files=True, type=['xml', 'zip'])

if st.button("Faturaları Birleştir ve PDF Yap", type="primary"):
    if not uploaded_files:
        st.warning("Lütfen en az bir dosya yükleyin.")
    else:
        with st.spinner('Motor hazırlanıyor ve faturalar işleniyor, lütfen bekleyin...'):
            with tempfile.TemporaryDirectory() as work_dir:
                xml_dosyalari = []
                
                # Dosyaları sunucuya kaydet
                for uploaded_file in uploaded_files:
                    hedef_yol = os.path.join(work_dir, uploaded_file.name)
                    with open(hedef_yol, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Klasördeki tüm iç içe ZIP'leri Matruşka gibi çıkar
                tum_arsivleri_ac(work_dir)

                # XML'leri (Uzantısız olanlar dahil) ara ve topla
                for root, _, files in os.walk(work_dir):
                    for file in files:
                        tam_yol = os.path.join(root, file)
                        # Eğer uzantısı XML ise listeye ekle
                        if file.lower().endswith('.xml'):
                            if tam_yol not in xml_dosyalari:
                                xml_dosyalari.append(tam_yol)
                        # Eğer uzantısı yoksa veya HTML değilse içine bak
                        elif not file.lower().endswith(('.pdf', '.html', '.htm', '.xslt', '.png', '.jpg')):
                            try:
                                with open(tam_yol, 'rb') as tf:
                                    head = tf.read(250)
                                    # Fatura kodu veya XML başlığı varsa XML say
                                    if b'<?xml' in head or b'<Invoice' in head:
                                        if tam_yol not in xml_dosyalari:
                                            xml_dosyalari.append(tam_yol)
                            except: pass

                if not xml_dosyalari:
                    st.error("Yüklenen dosyaların içinde (veya ZIP'lerin derinliklerinde) geçerli bir XML bulunamadı.")
                else:
                    merger = PdfMerger()
                    basarili_sayisi = 0
                    basarisiz_sayisi = 0
                    
                    varsayilan_sablon = "sablon.xslt" if os.path.exists("sablon.xslt") else None
                    
                    for idx, xml_yol in enumerate(xml_dosyalari):
                        pdf_cikti = os.path.join(work_dir, f"fatura_{idx}.pdf")
                        if xml_to_pdf(xml_yol, pdf_cikti, fallback_xslt_path=varsayilan_sablon):
                            merger.append(pdf_cikti)
                            basarili_sayisi += 1
                        else:
                            basarisiz_sayisi += 1
                            
                    if basarili_sayisi > 0:
                        final_pdf_yolu = os.path.join(work_dir, "BIRLESTIRILMIS_FATURALAR.pdf")
                        merger.write(final_pdf_yolu)
                        merger.close()
                        
                        st.success(f"İşlem Tamamlandı! {basarili_sayisi} adet fatura birleştirildi.")
                        if basarisiz_sayisi > 0:
                            st.info(f"Not: {basarisiz_sayisi} adet fatura (tasarım şablonu olmadığı için) atlandı.")
                            
                        with open(final_pdf_yolu, "rb") as pdf_file:
                            PDFbyte = pdf_file.read()
                        
                        st.download_button(
                            label="📥 Birleştirilmiş PDF'i İndir",
                            data=PDFbyte,
                            file_name="BIRLESTIRILMIS_FATURALAR.pdf",
                            mime="application/octet-stream"
                        )
                    else:
                        st.error("Hiçbir fatura dönüştürülemedi. Dosyalar bozuk veya şablon barındırmıyor olabilir.")

st.markdown("---")
st.caption("Güvenlik Notu: Yüklenen tüm faturalar ve oluşturulan PDF'ler, işlem biter bitmez sunucudan kalıcı olarak silinir.")
