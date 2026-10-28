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
import time
import pandas as pd
from openpyxl.styles import numbers

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

# Sayfa düzenini geniş ekran yapalım
st.set_page_config(page_title="E-Fatura Toplu PDF ve Excel Dönüştürücü", page_icon="📄", layout="wide")

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

# --- 1. EXCEL (FATURA BAŞLIKLARI) İÇİN VERİ AYIKLAMA ---
def fatura_verilerini_ayikla(xml_path):
    try:
        with open(xml_path, 'rb') as f:
            raw_content = f.read()
        xml_parser = etree.XMLParser(recover=True, no_network=True, resolve_entities=False)
        tree = etree.fromstring(raw_content, parser=xml_parser)
        
        def get_text_by_tag_name(tag_name, parent=None):
            xpath = f".//*[local-name()='{tag_name}']"
            elements = (parent if parent is not None else tree).xpath(xpath)
            return elements[0].text.strip() if elements and elements[0].text else ""

        tarih_xml = get_text_by_tag_name('IssueDate')
        tarih = ""
        if tarih_xml and re.match(r'\d{4}-\d{2}-\d{2}', tarih_xml):
            y, m, d = tarih_xml.split('-')
            tarih = f"{d}.{m}.{y}"

        fatura_no = get_text_by_tag_name('ID')
        fatura_turu = get_text_by_tag_name('InvoiceTypeCode') or "SATIS"
        
        vkn = ""
        customer_party = tree.xpath(".//*[local-name()='AccountingCustomerParty']")
        if customer_party:
            vkn_raw = get_text_by_tag_name('CompanyID', customer_party[0]) or get_text_by_tag_name('ID', customer_party[0])
            if vkn_raw:
                vkn = str(vkn_raw).replace('.0', '').strip()
        
        satici_unvani = ""
        supplier_party = tree.xpath(".//*[local-name()='AccountingSupplierParty']")
        if supplier_party:
            party_name = supplier_party[0].xpath(".//*[local-name()='PartyName']")
            if party_name:
                satici_unvani = get_text_by_tag_name('Name', party_name[0])
            if not satici_unvani:
                satici_unvani = get_text_by_tag_name('Name', supplier_party[0])

        tevkifat_orani = ""
        genel_toplam = get_text_by_tag_name('PayableAmount')
        
        kdv_dict = {
            "%1'lik KDV": None, "%8'lik KDV": None, "%10'lik KDV": None, "%18'lik KDV": None, "%20'lik KDV": None,
            "%1'lik Matrah": None, "%8'lik Matrah": None, "%10'lik Matrah": None, "%18'lik Matrah": None, "%20'lik Matrah": None
        }
        
        tax_subtotals = tree.xpath(".//*[local-name()='TaxSubtotal']")
        for subtotal in tax_subtotals:
            tax_code = get_text_by_tag_name('TaxTypeCode', subtotal)
            oran = get_text_by_tag_name('Percent', subtotal)
            matrah = get_text_by_tag_name('TaxableAmount', subtotal)
            vergi = get_text_by_tag_name('TaxAmount', subtotal)
            
            if tax_code and '9015' in tax_code:
                tevkifat_orani = oran
                continue 
                
            if oran and matrah:
                try:
                    oran_int = int(float(oran))
                    kdv_dict[f"%{oran_int}'lik KDV"] = float(vergi) if vergi else 0.0
                    kdv_dict[f"%{oran_int}'lik Matrah"] = float(matrah)
                except: pass
                    
        return {
            "Fatura Tarihi": tarih,
            "Fatura Numarası": fatura_no,
            "Fatura Türü": fatura_turu,
            "VKN TCKN": vkn,
            "Satıcı Ünvanı": satici_unvani,
            "Tevkifat Oranı": tevkifat_orani,
            **kdv_dict,
            "Toplam": float(genel_toplam) if genel_toplam else 0.0
        }
    except Exception:
        return None

# --- 2. EXCEL (ÜRÜN DETAYLARI) İÇİN VERİ AYIKLAMA ---
def fatura_urunlerini_ayikla(xml_path):
    urun_listesi = []
    try:
        with open(xml_path, 'rb') as f:
            raw_content = f.read()
        xml_parser = etree.XMLParser(recover=True, no_network=True, resolve_entities=False)
        tree = etree.fromstring(raw_content, parser=xml_parser)
        
        def get_text_by_tag_name(tag_name, parent=None):
            xpath = f".//*[local-name()='{tag_name}']"
            elements = (parent if parent is not None else tree).xpath(xpath)
            return elements[0].text.strip() if elements and elements[0].text else ""

        fatura_no = get_text_by_tag_name('ID')
        
        # Satıcı Ünvanı
        satici_unvani = ""
        supplier_party = tree.xpath(".//*[local-name()='AccountingSupplierParty']")
        if supplier_party:
            party_name = supplier_party[0].xpath(".//*[local-name()='PartyName']")
            if party_name:
                satici_unvani = get_text_by_tag_name('Name', party_name[0])
            if not satici_unvani:
                satici_unvani = get_text_by_tag_name('Name', supplier_party[0])
        
        invoice_lines = tree.xpath(".//*[local-name()='InvoiceLine']")
        for line in invoice_lines:
            urun_adi = ""
            items = line.xpath(".//*[local-name()='Item']")
            for item in items:
                name = get_text_by_tag_name('Name', item)
                desc = get_text_by_tag_name('Description', item)
                if name:
                    urun_adi = name
                    break
                elif desc:
                    urun_adi = desc
                    break
            
            # Eğer ürün adı boşsa satır notuna bak
            if not urun_adi:
                urun_adi = get_text_by_tag_name('Note', line)

            # Filtreleme (Alıcı Ödemeli gibi anlamsız ifadeleri geç)
            if not urun_adi or urun_adi.lower() in ["alıcı ödemeli", "alici odemeli"]:
                continue

            miktar = get_text_by_tag_name('InvoicedQuantity', line) or get_text_by_tag_name('Quantity', line)
            birim_fiyat = get_text_by_tag_name('PriceAmount', line)
            toplam_tutar = get_text_by_tag_name('LineExtensionAmount', line)
            
            try:
                miktar_f = float(miktar) if miktar else 0.0
                birim_f = float(birim_fiyat) if birim_fiyat else 0.0
                toplam_f = float(toplam_tutar) if toplam_tutar else 0.0
            except:
                miktar_f, birim_f, toplam_f = 0.0, 0.0, 0.0

            urun_listesi.append({
                "Fatura Numarası": fatura_no,
                "Satıcı Ünvanı": satici_unvani,
                "Ürün / Hizmet Adı": urun_adi,
                "Miktar": miktar_f,
                "Birim Fiyat": birim_f,
                "Toplam Tutar": toplam_f
            })
    except Exception:
        pass
    return urun_listesi

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

        if not xslt_content:
            return False, "Şablon bulunamadı."

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
            if xslt_content:
                transform = sablon_derle(xslt_content)
        except Exception:
            pass

        if transform is None and fallback_xslt_path and os.path.exists(fallback_xslt_path):
            try:
                with open(fallback_xslt_path, 'rb') as f_sablon:
                    transform = sablon_derle(f_sablon.read())
            except Exception:
                pass

        if transform is None:
            return False, "Şablon kilitlendi."

        html_dom = transform(tree)
        html_str = str(html_dom)
        
        def resim_indirici(match):
            full_tag = match.group(0)
            resim_url = match.group(1)
            
            try:
                if 'qr.sovostr.com/qr?data=' in resim_url or fatura_uuid:
                    if fatura_uuid:
                        dogrulama_linki = f"https://earsivportal.efatura.gov.tr/intragrs/sorgula.jsp?ettn={fatura_uuid}"
                    else:
                        qr_data = resim_url.split('data=', 1)[-1]
                        dogrulama_linki = html.unescape(urllib.parse.unquote(qr_data))
                    
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
                if not (os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 10):
                    raise e
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


# Session state başlatma
if 'pdf_data' not in st.session_state: st.session_state.pdf_data = None
if 'excel_data' not in st.session_state: st.session_state.excel_data = None
if 'urun_excel_data' not in st.session_state: st.session_state.urun_excel_data = None
if 'islem_tamamlandi' not in st.session_state: st.session_state.islem_tamamlandi = False
if 'basarili_sayisi' not in st.session_state: st.session_state.basarili_sayisi = 0
if 'basarisiz_sayisi' not in st.session_state: st.session_state.basarisiz_sayisi = 0
if 'hata_loglari' not in st.session_state: st.session_state.hata_loglari = []

# ----- WEB ARAYÜZÜ -----
st.title("🚀 E-Fatura Toplu PDF ve Excel Dönüştürücü")
st.markdown("XML faturalarınızı veya faturaları içeren ZIP arşivlerini buraya yükleyin. Sistem hepsini **tarih sırasına göre** tek bir PDF ve detaylı bir **Excel tablosu** olarak size sunacaktır.")

uploaded_files = st.file_uploader("XML veya ZIP Dosyalarını Seçin", accept_multiple_files=True, type=['xml', 'zip'])

if st.button("Faturaları Birleştir, PDF ve Excel Yap", type="primary"):
    if not uploaded_files:
        st.warning("Lütfen en az bir dosya yükleyin.")
    else:
        # Önceki işlem verilerini sıfırla
        st.session_state.pdf_data = None
        st.session_state.excel_data = None
        st.session_state.urun_excel_data = None
        st.session_state.islem_tamamlandi = False
        st.session_state.basarili_sayisi = 0
        st.session_state.basarisiz_sayisi = 0
        st.session_state.hata_loglari = []

        with st.spinner('Motor hazırlanıyor ve faturalar işleniyor, lütfen bekleyin...'):
            with tempfile.TemporaryDirectory() as work_dir:
                xml_dosyalari = []
                excel_verileri = []
                urun_excel_verileri = []
                
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
                        
                        # 1. PDF Dönüşümü
                        basarili_mi, hata_mesaji = xml_to_pdf(xml_yol, pdf_cikti, fallback_xslt_path=varsayilan_sablon, bim_xslt_path=bim_sablon)
                        
                        if basarili_mi:
                            merger.append(pdf_cikti)
                            basarili_sayisi += 1
                        else:
                            basarisiz_sayisi += 1
                            hata_loglari.append(f"Fatura ({os.path.basename(xml_yol)}): {hata_mesaji}")
                        
                        # 2. Fatura Özet Excel Verisi
                        fatura_data = fatura_verilerini_ayikla(xml_yol)
                        if fatura_data:
                            excel_verileri.append(fatura_data)
                            
                        # 3. Ürün Detay Excel Verisi
                        urun_data = fatura_urunlerini_ayikla(xml_yol)
                        if urun_data:
                            urun_excel_verileri.extend(urun_data)
                            
                    if basarili_sayisi > 0 or excel_verileri:
                        # PDF Birleştirme ve Kaydetme
                        if basarili_sayisi > 0:
                            final_pdf_yolu = os.path.join(work_dir, "BIRLESTIRILMIS_FATURALAR.pdf")
                            merger.write(final_pdf_yolu)
                            with open(final_pdf_yolu, "rb") as pdf_file:
                                st.session_state.pdf_data = pdf_file.read()
                        merger.close()
                        
                        # --- FATURA LİSTESİ EXCEL OLUŞTURMA ---
                        if excel_verileri:
                            df = pd.DataFrame(excel_verileri)
                            df = df.dropna(axis=1, how='all')
                            for col in df.columns:
                                if df[col].astype(str).str.strip().eq('').all() or df[col].astype(str).eq('None').all():
                                    df = df.drop(columns=[col])
                                    
                            oncelikli_sutunlar = ["Fatura Tarihi", "Fatura Numarası", "Fatura Türü", "VKN TCKN", "Satıcı Ünvanı", "Tevkifat Oranı", "Özel Matrah"]
                            matrah_sirasi = ["%1'lik Matrah", "%8'lik Matrah", "%10'lik Matrah", "%18'lik Matrah", "%20'lik Matrah"]
                            kdv_sirasi = ["%1'lik KDV", "%8'lik KDV", "%10'lik KDV", "%18'lik KDV", "%20'lik KDV"]
                            
                            mevcut_matrahlar = [c for c in matrah_sirasi if c in df.columns]
                            mevcut_kdvler = [c for c in kdv_sirasi if c in df.columns]
                            
                            son_sutunlar = oncelikli_sutunlar + mevcut_matrahlar + mevcut_kdvler + ["Toplam"]
                            df = df[[c for c in son_sutunlar if c in df.columns]]
                            
                            excel_cikti_yolu = os.path.join(work_dir, "FATURA_LISTESI.xlsx")
                            with pd.ExcelWriter(excel_cikti_yolu, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name='FATURALAR')
                                worksheet = writer.sheets['FATURALAR']
                                for i, col in enumerate(df.columns):
                                    # Güvenli sütun genişliği hesaplama
                                    max_len = df[col].astype(str).str.len().max()
                                    if pd.isna(max_len): max_len = 0
                                    max_len = max(max_len, len(str(col))) + 2
                                    
                                    col_letter = chr(65 + i) if i < 26 else chr(64 + i // 26) + chr(65 + i % 26)
                                    worksheet.column_dimensions[col_letter].width = max_len
                                    
                                    if any(x in col for x in ['Matrah', 'KDV', 'Toplam']):
                                        for row in range(2, len(df) + 2):
                                            worksheet.cell(row=row, column=i+1).number_format = '#,##0.00'
                            
                            with open(excel_cikti_yolu, "rb") as excel_file:
                                st.session_state.excel_data = excel_file.read()

                        # --- ÜRÜN LİSTESİ EXCEL OLUŞTURMA ---
                        if urun_excel_verileri:
                            df_urun = pd.DataFrame(urun_excel_verileri)
                            
                            urun_excel_yolu = os.path.join(work_dir, "URUN_LISTESI.xlsx")
                            with pd.ExcelWriter(urun_excel_yolu, engine='openpyxl') as writer:
                                df_urun.to_excel(writer, index=False, sheet_name='ÜRÜNLER')
                                worksheet = writer.sheets['ÜRÜNLER']
                                for i, col in enumerate(df_urun.columns):
                                    # Güvenli sütun genişliği hesaplama
                                    max_len = df_urun[col].astype(str).str.len().max()
                                    if pd.isna(max_len): max_len = 0
                                    max_len = max(max_len, len(str(col))) + 2
                                    
                                    col_letter = chr(65 + i) if i < 26 else chr(64 + i // 26) + chr(65 + i % 26)
                                    worksheet.column_dimensions[col_letter].width = max_len
                                    
                                    if any(x in col for x in ['Miktar', 'Fiyat', 'Tutar']):
                                        for row in range(2, len(df_urun) + 2):
                                            worksheet.cell(row=row, column=i+1).number_format = '#,##0.00'
                            
                            with open(urun_excel_yolu, "rb") as u_file:
                                st.session_state.urun_excel_data = u_file.read()

                        st.session_state.basarili_sayisi = basarili_sayisi
                        st.session_state.basarisiz_sayisi = basarisiz_sayisi
                        st.session_state.hata_loglari = hata_loglari
                        st.session_state.islem_tamamlandi = True
                        
                        st.rerun()

# İşlem tamamlandıysa butonları göster
if st.session_state.islem_tamamlandi:
    st.success(f"✅ İşlem Tamamlandı! {st.session_state.basarili_sayisi} adet fatura PDF'e dönüştürüldü ve Excel listeleri oluşturuldu.")
    
    if st.session_state.basarisiz_sayisi > 0:
        st.info(f"Not: {st.session_state.basarisiz_sayisi} adet fatura PDF'e dönüştürülemedi.")
        with st.expander("Hata Detaylarını Görmek İçin Tıklayın"):
            for log in st.session_state.hata_loglari:
                st.write(log)
                
    # 1. ve 2. Butonlar (Yan Yana)
    col1, col2 = st.columns(2)
    if st.session_state.pdf_data:
        with col1:
            st.download_button(
                label="📥 Birleştirilmiş PDF İndir",
                data=st.session_state.pdf_data,
                file_name="BIRLESTIRILMIS_FATURALAR.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    if st.session_state.excel_data:
        with col2:
            st.download_button(
                label="📊 Fatura Özet Excel İndir",
                data=st.session_state.excel_data,
                file_name="FATURA_LISTESI.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    # 3. Buton (Alt Tarafa, Tam Genişlik) - Mavi Çizdiğiniz Yer
    if st.session_state.urun_excel_data:
        st.download_button(
            label="📦 Ürün/Hizmet Detay Excel İndir",
            data=st.session_state.urun_excel_data,
            file_name="URUN_LISTESI.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

st.markdown("---")
st.caption("Güvenlik Notu: Yüklenen tüm faturalar ve oluşturulan dosyalar, işlem biter bitmez sunucudan kalıcı olarak silinir.")
