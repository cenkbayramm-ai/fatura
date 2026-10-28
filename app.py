import streamlit as st
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
    st.error(f"🚨 PDF Motoru İndirilirken Hata: {str(e)}")
# ------------------------------------------------------

st.set_page_config(page_title="E-Fatura PDF Çevirici", page_icon="📄", layout="centered")

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
                                with zipfile.ZipFile(mem_
