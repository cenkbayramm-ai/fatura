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

st.set_page_config(page_title="E-Fatura Akıllı Asistan", page_icon="📄", layout="wide")

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

        # Fatura Özeti
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
                '
