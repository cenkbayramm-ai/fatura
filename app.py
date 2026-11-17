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
import urllib.parse
import html
from lxml import etree
import pdfkit
from PyPDF2 import PdfMerger
import pandas as pd
import time

# --- YOL AYARLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = tempfile.gettempdir()
WK_DIR = os.path.join(TEMP_DIR, "wkhtmltox")
WK_PATH = os.path.join(WK_DIR, "bin", "wkhtmltopdf")

# --- LİNUX İÇİN PDF MOTORUNU TEMP KLASÖRÜNE KURMA ---
@st.cache_resource
def motoru_indir():
    if not os.path.exists(WK_PATH):
        tar_yolu = os.path.join(TEMP_DIR, "wk.tar.xz")
        for _ in range(3):
            try:
                urllib.request.urlretrieve("https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz", tar_yolu)
                subprocess.run(["tar", "xf", tar_yolu, "-C", TEMP_DIR], check=True)
                subprocess.run(["chmod", "+x", WK_PATH], check=True)
                break
            except Exception:
                time.sleep(2)

try:
    motoru_indir()
except Exception:
    pass

st.set_page_config(page_title="E-Fatura Akıllı Asistan", page_icon="💼", layout="wide")

# ==========================================
# SESSION STATE (KALICI BELLEK) BAŞLATMA
# ==========================================
if 'islem_tamam' not in st.session_state:
    st.session_state.islem_tamam = False
if 'pdf_veri' not in st.session_state:
    st.session_state.pdf_veri = None
if 'csv_veri' not in st.session_state:
    st.session_state.csv_veri = None
if 'fatura_excel_veri' not in st.session_state:
    st.session_state.fatura_excel_veri = None
if 'urun_excel_veri' not in st.session_state:
    st.session_state.urun_excel_veri = None
if 'hata_loglari' not in st.session_state:
    st.session_state.hata_loglari = []

def session_sifirla():
    st.session_state.islem_tamam = False
    st.session_state.pdf_veri = None
    st.session_state.csv_veri = None
    st.session_state.fatura_excel_veri = None
    st.session_state.urun_excel_veri = None
    st.session_state.hata_loglari = []

# ==========================================
# YARDIMCI FONKSİYONLAR
# ==========================================
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

def verileri_cikar(xml_path):
    try:
        with open(xml_path, 'rb') as f:
            raw_content = f.read()
        if raw_content.startswith(b'\xef\xbb\xbf'):
            raw_content = raw_content[3:]
            
        xml_parser = etree.XMLParser(recover=True, no_network=True, resolve_entities=False)
        tree = etree.fromstring(raw_content, parser=xml_parser)
        namespaces = {
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        }

        f_tarih = tree.findtext('.//cbc:IssueDate', namespaces=namespaces, default='')
        if f_tarih:
            parts = f_tarih.split('-')
            if len(parts) == 3: f_tarih = f"{parts[2]}.{parts[1]}.{parts[0]}"

        f_no = tree.findtext('.//cbc:ID', namespaces=namespaces, default='')

        firma_ismi = tree.findtext('.//cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name', namespaces=namespaces, default='').strip()
        if not firma_ismi:
            first = tree.findtext('.//cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:FirstName', namespaces=namespaces, default='').strip()
            last = tree.findtext('.//cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:FamilyName', namespaces=namespaces, default='').strip()
            firma_ismi = f"{first} {last}".strip()

        vkn_tckn = tree.findtext('.//cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID', namespaces=namespaces, default='').strip()
        toplam = float(tree.findtext('.//cac:LegalMonetaryTotal/cbc:PayableAmount', namespaces=namespaces, default='0'))
        
        matrah1 = matrah10 = matrah20 = 0.0
        kdv1 = kdv10 = kdv20 = 0.0

        for tax_subtotal in tree.findall('.//cac:TaxTotal/cac:TaxSubtotal', namespaces=namespaces):
            tax_code = tax_subtotal.findtext('.//cac:TaxScheme/cbc:TaxTypeCode', namespaces=namespaces, default='')
            if tax_code == '0015':
                percent = float(tax_subtotal.findtext('cbc:Percent', namespaces=namespaces, default='0'))
                taxable = float(tax_subtotal.findtext('cbc:TaxableAmount', namespaces=namespaces, default='0'))
                tax = float(tax_subtotal.findtext('cbc:TaxAmount', namespaces=namespaces, default='0'))

                if percent == 1.0:
                    matrah1 += taxable
                    kdv1 += tax
                elif percent == 10.0:
                    matrah10 += taxable
                    kdv10 += tax
                elif percent == 20.0:
                    matrah20 += taxable
                    kdv20 += tax

        bedel = matrah1 + matrah10 + matrah20
        kdv_toplam = kdv1 + kdv10 + kdv20

        # Luca Fatura Özeti
        fatura_dict = {
            'F.TARİH': f_tarih,
            'F.NO': f_no,
            'VKN/TCKN': vkn_tckn,
            'FİRMA İSMİ': firma_ismi,
            'BEDEL': round(bedel, 2),
            'KDV': round(kdv_toplam, 2),
            'TOPLAM': round(toplam, 2),
            'MATRAH1 ': round(matrah1, 2),
            'KDV1': round(kdv1, 2),
            'MATRAH10': round(matrah10, 2),
            'KDV10': round(kdv10, 2),
            'MATRAH20': round(matrah20, 2),
            'KDV20': round(kdv20, 2)
        }

        # Ürün (Kalem) Listesi
        urun_listesi = []
        for line in tree.findall('.//cac:InvoiceLine', namespaces=namespaces):
            urun_kodu = line.findtext('.//cac:Item/cac:SellersItemIdentification/cbc:ID', namespaces=namespaces, default='').strip()
            urun_adi = line.findtext('.//cac:Item/cbc:Name', namespaces=namespaces, default='').strip()
            miktar = float(line.findtext('.//cbc:InvoicedQuantity', namespaces=namespaces, default='0'))
            birim_fiyat = float(line.findtext('.//cac:Price/cbc:PriceAmount', namespaces=namespaces, default='0'))
            iskonto = float(line.findtext('.//cac:AllowanceCharge/cbc:Amount', namespaces=namespaces, default='0'))
            kdv_orani = float(line.findtext('.//cac:TaxTotal/cac:TaxSubtotal/cbc:Percent', namespaces=namespaces, default='0'))
            tutar = float(line.findtext('.//cbc:LineExtensionAmount', namespaces=namespaces, default='0'))

            urun_listesi.append({
                'Fatura Tarihi': f_tarih,
                'Fatura No': f_no,
                'Alıcı VKN/TCKN': vkn_tckn,
                'Alıcı Firma': firma_ismi,
                'Ürün Kodu': urun_kodu,
                'Ürün Adı': urun_adi,
                'Miktar': round(miktar, 2),
                'Birim Fiyat': round(birim_fiyat, 4),
                'İskonto Tutarı': round(iskonto, 2),
                'KDV Oranı': f"%{int(kdv_orani)}",
                'KDV Hariç Tutar': round(tutar, 2)
            })

        return fatura_dict, urun_listesi
    except Exception:
        return None, []

def xml_to_pdf(xml_path, output_pdf_path, fallback_xslt_path=None, bim_xslt_path=None):
    try:
        with open(xml_path, 'rb') as f:
            raw_content = f.read()
            
        if raw_content.startswith(b'\xef\xbb\xbf'):
            raw_content = raw_content[3:]
            
        is_bim = b'1750051846' in raw_content or b'earsivbimxslt' in raw_content
            
        raw_content = re.sub(br'<\?xml-stylesheet[^>]*\?>', b'', raw_content)
        xml_parser = etree.XMLParser(recover=True, no_network=True, resolve_entities=False)
        tree = etree.fromstring(raw_content, parser=xml_parser)
        
        # Küsurat Temizliği (Görsel İçin)
        for elem in tree.iter():
            if elem.text and type(elem.tag) == str:
                tag_name = etree.QName(elem).localname
                if any(x in tag_name for x in ['Amount', 'Quantity', 'Price', 'Percent', 'Rate']):
                    metin = elem.text.strip()
                    if re.match(r'^-?\d+\.\d{3,}$', metin):
                        try:
                            deger = float(metin)
                            if 'Price' in tag_name:
                                elem.text = f"{deger:.4f}".rstrip('0').rstrip('.')
                                if not elem.text: elem.text = "0"
                            elif 'Quantity' in tag_name:
                                elem.text = f"{deger:.2f}".rstrip('0').rstrip('.')
                                if not elem.text: elem.text = "0"
                            else:
                                elem.text = f"{deger:.2f}"
                        except Exception:
                            pass
        
        namespaces = {
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        }
        uuid_node = tree.find('.//cbc:UUID', namespaces)
        fatura_uuid = uuid_node.text.strip() if uuid_node is not None and uuid_node.text else ""

        xslt_content = None
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

        if not xslt_content and fallback_xslt_path and os.path.exists(fallback_xslt_path):
            with open(fallback_xslt_path, 'rb') as f_sablon:
                xslt_content = f_sablon.read()

        if not xslt_content: return False, "Şablon bulunamadı."

        transform = None
        xslt_parser = etree.XMLParser(recover=True, no_network=True)
        def sablon_derle(content_bytes):
            xslt_str = content_bytes.decode('utf-8', errors='ignore')
            xslt_str = re.sub(r'<\?xml.*\?>', '', xslt_str)
            xslt_str = re.sub(r'<xsl:import[^>]+href=["\']https?://[^"\']+["\'][^>]*?/?>', '', xslt_str, flags=re.IGNORECASE)
            xslt_str = re.sub(r'<xsl:include[^>]+href=["\']https?://[^"\']+["\'][^>]*?/?>', '', xslt_str, flags=re.IGNORECASE)
            xslt_root = etree.fromstring(xslt_str.encode('utf-8'), parser=xslt_parser)
            return etree.XSLT(xslt_root)

        try:
            if xslt_content: transform = sablon_derle(xslt_content)
        except Exception: pass
        if transform is None and fallback_xslt_path and os.path.exists(fallback_xslt_path):
            try:
                with open(fallback_xslt_path, 'rb') as f_sablon:
                    transform = sablon_derle(f_sablon.read())
            except Exception: pass

        if transform is None: return False, "Şablon kilitlendi."

        html_dom = transform(tree)
        html_str = str(html_dom)
        
        # GİB Karekod ve Resim İndirici
        def resim_indirici(match):
            full_tag = match.group(0)
            resim_url = match.group(1)
            try:
                if 'qr.sovostr.com/qr?data=' in resim_url or fatura_uuid:
                    if fatura_uuid: dogrulama_linki = f"https://earsivportal.efatura.gov.tr/intragrs/sorgula.jsp?ettn={fatura_uuid}"
                    else: dogrulama_linki = html.unescape(urllib.parse.unquote(resim_url.split('data=', 1)[-1]))
                    
                    safe_data = urllib.parse.quote(dogrulama_linki)
                    hedef_url = f"https://api.qrserver.com/v1/create-qr-code/?size=110x110&data={safe_data}"
                    yeni_tag_format = '<img src="{yeni_src}" style="width: 110px; height: 110px;" alt="QR Code" align="right" />'
                else:
                    hedef_url = urllib.parse.quote(resim_url, safe=":/&?=")
                    yeni_tag_format = full_tag.replace(resim_url, "{yeni_src}")
                    
                req = urllib.request.Request(hedef_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as response:
                    img_data = response.read()
                    
                ext = "png"
                if "jpeg" in resim_url.lower() or "jpg" in resim_url.lower(): ext = "jpeg"
                yeni_src = f"data:image/{ext};base64,{base64.b64encode(img_data).decode('utf-8')}"
                return yeni_tag_format.format(yeni_src=yeni_src)
            except Exception:
                return full_tag 

        html_str = re.sub(r'<img[^>]*?src=["\'](https?://[^"\']+)["\'][^>]*>', resim_indirici, html_str, flags=re.IGNORECASE)
        html_str = re.sub(r'href=["\']https?://[^"\']+\.css["\']', 'href=""', html_str, flags=re.IGNORECASE)
        
        config = pdfkit.configuration(wkhtmltopdf=WK_PATH)
        options = {
            'page-size': 'A4', 
            'encoding': "UTF-8", 
            'enable-local-file-access': "",
            'enable-javascript': "",
            'javascript-delay': 500,
            'no-outline': None, 
            'quiet': '',
            'load-error-handling': 'ignore',
            'load-media-error-handling': 'ignore'
        }
        
        try:
            try:
                pdfkit.from_string(html_str, output_pdf_path, configuration=config, options=options)
            except IOError as e:
                if not (os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 10): raise e
        except Exception:
            if fallback_xslt_path and os.path.exists(fallback_xslt_path):
                with open(fallback_xslt_path, 'rb') as f_sablon:
                    transform_yedek = sablon_derle(f_sablon.read())
                    html_str_yedek = str(transform_yedek(tree))
                    html_str_yedek = re.sub(r'<img[^>]*?src=["\'](https?://[^"\']+)["\'][^>]*>', resim_indirici, html_str_yedek, flags=re.IGNORECASE)
                    pdfkit.from_string(html_str_yedek, output_pdf_path, configuration=config, options=options)
            else:
                return False, "PDF Motoru çöktü."
        
        if not os.path.exists(output_pdf_path) or os.path.getsize(output_pdf_path) < 10:
            return False, "PDF dosyası fiziksel olarak oluşturulamadı."
            
        return True, ""
    except Exception as e:
        return False, f"Teknik Hata: {str(e)}"

# ==========================================
# SOL MENÜ (SIDEBAR) VE ANA YAPI
# ==========================================
st.sidebar.title("⚙️ Fatura İşlem Merkezi")

uploaded_files = st.sidebar.file_uploader("Fatura Arşivlerinizi Seçin (XML/ZIP)", accept_multiple_files=True, type=['xml', 'zip'])
if st.sidebar.button("🚀 Dosyaları İşle", type="primary"):
    if not uploaded_files:
        st.sidebar.warning("Lütfen işlem yapmadan önce dosya yükleyin.")
    else:
        session_sifirla() # Yeni işlemde eski belleği temizle
        with st.spinner('Tüm dosyalar okunuyor ve arka planda işleniyor...'):
            with tempfile.TemporaryDirectory() as work_dir:
                xml_dosyalari = []
                for uploaded_file in uploaded_files:
                    hedef_yol = os.path.join(work_dir, uploaded_file.name)
                    with open(hedef_yol, "wb") as f: f.write(uploaded_file.getbuffer())
                
                tum_arsivleri_ac(work_dir)

                for root, _, files in os.walk(work_dir):
                    for file in files:
                        tam_yol = os.path.join(root, file)
                        if file.lower().endswith('.xml'):
                            if tam_yol not in xml_dosyalari: xml_dosyalari.append(tam_yol)
                        elif not file.lower().endswith(('.pdf', '.html', '.htm', '.xslt', '.png', '.jpg')):
                            try:
                                with open(tam_yol, 'rb') as tf:
                                    head = tf.read(250)
                                    if b'<?xml' in head or b'<Invoice' in head:
                                        if tam_yol not in xml_dosyalari: xml_dosyalari.append(tam_yol)
                            except: pass

                if not xml_dosyalari:
                    st.sidebar.error("Yüklenen dosyaların içinde geçerli bir XML bulunamadı.")
                else:
                    xml_dosyalari.sort(key=lambda x: faturanin_tarihini_bul(x))
                    merger = PdfMerger()
                    basarili_sayisi = 0
                    
                    fatura_listesi = []
                    urun_listesi = []
                    
                    varsayilan_sablon = os.path.join(BASE_DIR, "sablon.xslt")
                    bim_sablon = os.path.join(BASE_DIR, "bim_sablon.xslt")
                    
                    for idx, xml_yol in enumerate(xml_dosyalari):
                        fatura_verisi, urunler = verileri_cikar(xml_yol)
                        if fatura_verisi: fatura_listesi.append(fatura_verisi)
                        if urunler: urun_listesi.extend(urunler)

                        pdf_cikti = os.path.join(work_dir, f"fatura_{idx}.pdf")
                        basarili_mi, hata_mesaji = xml_to_pdf(xml_yol, pdf_cikti, fallback_xslt_path=varsayilan_sablon, bim_xslt_path=bim_sablon)
                        
                        if basarili_mi:
                            merger.append(pdf_cikti)
                            basarili_sayisi += 1
                        else:
                            st.session_state.hata_loglari.append(f"Fatura ({os.path.basename(xml_yol)}): {hata_mesaji}")
                            
                    if basarili_sayisi > 0:
                        # 1. PDF Belleğe Kayıt
                        final_pdf_yolu = os.path.join(work_dir, "BIRLESTIRILMIS.pdf")
                        merger.write(final_pdf_yolu)
                        merger.close()
                        with open(final_pdf_yolu, "rb") as pdf_file:
                            st.session_state.pdf_veri = pdf_file.read()
                        
                        # 2. Fatura ve Ürün Verilerini Excel & CSV Olarak Belleğe Kayıt
                        if fatura_listesi:
                            df_fatura = pd.DataFrame(fatura_listesi)
                            # CSV Formatı (Luca İçin - VKN Hariç Klasik Sütunlar)
                            luca_cols = ['F.TARİH', 'F.NO', 'FİRMA İSMİ', 'BEDEL', 'KDV', 'TOPLAM', 'MATRAH1 ', 'KDV1', 'MATRAH10', 'KDV10', 'MATRAH20', 'KDV20']
                            df_csv = df_fatura[luca_cols]
                            st.session_state.csv_veri = df_csv.to_csv(index=False, sep=';', decimal=',').encode('cp1254', errors='replace')
                            
                            # Excel Fatura Formatı
                            io_fatura = io.BytesIO()
                            df_fatura.to_excel(io_fatura, index=False, engine='openpyxl', sheet_name='Faturalar')
                            st.session_state.fatura_excel_veri = io_fatura.getvalue()
                            
                        if urun_listesi:
                            df_urun = pd.DataFrame(urun_listesi)
                            io_urun = io.BytesIO()
                            df_urun.to_excel(io_urun, index=False, engine='openpyxl', sheet_name='Ürünler')
                            st.session_state.urun_excel_veri = io_urun.getvalue()
                        
                        st.session_state.islem_tamam = True
                        st.sidebar.success(f"İşlem Tamamlandı! Menülerden sonuçları indirebilirsiniz.")
                    else:
                        st.sidebar.error("Hiçbir fatura dönüştürülemedi.")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📂 DOSYA ÇIKTILARI (MENÜ)",
    ("📄 1. PDF Dosyası", "📦 2. Ürün Excel Listesi", "📊 3. Fatura Excel Listesi", "📑 4. Luca CSV Aktarımı")
)

# ==========================================
# MENÜ İÇERİKLERİ
# ==========================================
if menu == "📄 1. PDF Dosyası":
    st.title("📄 Birleştirilmiş PDF Çıktısı")
    st.info("Bu sayfada, yüklediğiniz faturaların tek bir PDF dosyasında birleştirilmiş hali bulunur.")
    
    if st.session_state.islem_tamam and st.session_state.pdf_veri:
        b64 = base64.b64encode(st.session_state.pdf_veri).decode()
        js_kodu = f"""
        <script>
            var a = document.createElement('a');
            a.href = 'data:application/pdf;base64,{b64}';
            a.download = 'TOPLU_FATURALAR.pdf';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        </script>
        """
        components.html(js_kodu, height=0)
        
        st.download_button(
            label="📥 PDF Dosyasını İndir",
            data=st.session_state.pdf_veri,
            file_name="TOPLU_FATURALAR.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        if st.session_state.hata_loglari:
            with st.expander("⚠️ Dönüştürülemeyen Faturaların Logları (Hata Detayı)"):
                for log in st.session_state.hata_loglari: st.write(log)
    else:
        st.warning("Henüz bir işlem yapılmadı. Lütfen sol taraftaki menüden dosyalarınızı yükleyip 'Dosyaları İşle' butonuna basınız.")

elif menu == "📦 2. Ürün Excel Listesi":
    st.title("📦 Detaylı Ürün (Kalem) Listesi")
    st.info("Faturalarınızın içindeki tüm satılan ürünlerin dökümünü içeren Excel dosyasıdır.")
    
    if st.session_state.islem_tamam and st.session_state.urun_excel_veri:
        st.download_button(
            label="📥 Ürün Listesini Excel Olarak İndir (.xlsx)",
            data=st.session_state.urun_excel_veri,
            file_name="URUN_LISTESI.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        # Önizleme
        df_onizleme = pd.read_excel(io.BytesIO(st.session_state.urun_excel_veri))
        st.dataframe(df_onizleme, use_container_width=True)
    else:
        st.warning("Henüz bir işlem yapılmadı veya faturaların içinde ürün detayı bulunamadı.")

elif menu == "📊 3. Fatura Excel Listesi":
    st.title("📊 Fatura Özeti Excel Listesi")
    st.info("Faturalarınızın başlık, VKN ve genel toplam bilgilerini içeren standart Excel dökümüdür.")
    
    if st.session_state.islem_tamam and st.session_state.fatura_excel_veri:
        st.download_button(
            label="📥 Fatura Listesini Excel Olarak İndir (.xlsx)",
            data=st.session_state.fatura_excel_veri,
            file_name="FATURA_LISTESI.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        # Önizleme
        df_onizleme = pd.read_excel(io.BytesIO(st.session_state.fatura_excel_veri))
        st.dataframe(df_onizleme, use_container_width=True)
    else:
        st.warning("Henüz bir işlem yapılmadı. Lütfen sol taraftaki menüden dosyalarınızı yükleyin.")

elif menu == "📑 4. Luca CSV Aktarımı":
    st.title("📑 Luca Matrahlı Fatura Aktarımı")
    st.info("Luca muhasebe programına fiş/fatura aktarımı yapabilmeniz için (KDV'lerine göre ayrıştırılmış) özel CSV dosyasıdır.")
    
    if st.session_state.islem_tamam and st.session_state.csv_veri:
        st.download_button(
            label="📥 Luca CSV Dosyasını İndir",
            data=st.session_state.csv_veri,
            file_name="LUCA_AKTARIM.csv",
            mime="text/csv",
            use_container_width=True
        )
        # Önizleme
        df_onizleme = pd.read_csv(io.BytesIO(st.session_state.csv_veri), sep=';', encoding='cp1254')
        st.dataframe(df_onizleme, use_container_width=True)
    else:
        st.warning("Henüz bir işlem yapılmadı. Lütfen sol taraftaki menüden dosyalarınızı yükleyin.")
