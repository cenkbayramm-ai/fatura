<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" 
    xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
    <xsl:template match="/">
        <html>
            <head>
                <meta charset="utf-8"/>
                <style>
                    body { font-family: Arial, sans-serif; font-size: 12px; color: #333; }
                    .container { width: 100%; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .header { text-align: center; font-size: 18px; font-weight: bold; padding: 10px; border-bottom: 2px solid #333; margin-bottom: 20px; }
                    .info-table { width: 100%; margin-bottom: 20px; }
                    .info-table td { padding: 5px; vertical-align: top; }
                    .box { border: 1px solid #ccc; padding: 10px; border-radius: 5px; min-height: 90px; }
                    .lines-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                    .lines-table th, .lines-table td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 11px; }
                    .lines-table th { background-color: #f2f2f2; font-weight: bold; }
                    .totals-table { width: 45%; float: right; border-collapse: collapse; }
                    .totals-table td { border: 1px solid #ccc; padding: 6px; }
                    .totals-table .right { text-align: right; }
                    .totals-table .bold { font-weight: bold; background-color: #f9f9f9; }
                    .clear { clear: both; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <xsl:value-of select="//cbc:ProfileID"/> - <xsl:value-of select="//cbc:InvoiceTypeCode"/> FATURASI
                    </div>
                    
                    <table class="info-table">
                        <tr>
                            <td width="50%">
                                <div class="box">
                                    <strong>SATICI (GÖNDEREN):</strong><br/>
                                    <xsl:value-of select="//cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name"/><br/>
                                    VKN/TCKN: <xsl:value-of select="//cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID"/><br/>
                                    Vergi Dairesi: <xsl:value-of select="//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name"/>
                                </div>
                            </td>
                            <td width="50%">
                                <div class="box">
                                    <strong>ALICI (MÜŞTERİ):</strong><br/>
                                    <xsl:value-of select="//cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name"/><br/>
                                    VKN/TCKN: <xsl:value-of select="//cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID"/><br/>
                                    Vergi Dairesi: <xsl:value-of select="//cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name"/>
                                </div>
                            </td>
                        </tr>
                    </table>

                    <table class="info-table" style="border: 1px solid #ccc; border-radius: 5px;">
                        <tr>
                            <td><strong>Fatura No:</strong> <xsl:value-of select="//cbc:ID"/></td>
                            <td><strong>Tarih:</strong> <xsl:value-of select="//cbc:IssueDate"/></td>
                            <td><strong>Para Birimi:</strong> <xsl:value-of select="//cbc:DocumentCurrencyCode"/></td>
                        </tr>
                    </table>

                    <table class="lines-table">
                        <tr>
                            <th>Mal/Hizmet Cinsi</th>
                            <th>Miktar</th>
                            <th>Birim Fiyat</th>
                            <th>İskonto</th>
                            <th>KDV Oranı</th>
                            <th>Tutar</th>
                        </tr>
                        <xsl:for-each select="//cac:InvoiceLine">
                            <tr>
                                <td><xsl:value-of select="cac:Item/cbc:Name"/></td>
                                <td><xsl:value-of select="cbc:InvoicedQuantity"/> <xsl:value-of select="cbc:InvoicedQuantity/@unitCode"/></td>
                                <td><xsl:value-of select="cac:Price/cbc:PriceAmount"/></td>
                                <td><xsl:value-of select="cac:AllowanceCharge/cbc:Amount"/></td>
                                <td>%<xsl:value-of select="cac:TaxTotal/cac:TaxSubtotal/cbc:Percent"/></td>
                                <td><xsl:value-of select="cbc:LineExtensionAmount"/></td>
                            </tr>
                        </xsl:for-each>
                    </table>

                    <table class="totals-table">
                        <tr>
                            <td>Mal Hizmet Toplam Tutarı</td>
                            <td class="right"><xsl:value-of select="//cac:LegalMonetaryTotal/cbc:LineExtensionAmount"/></td>
                        </tr>
                        <tr>
                            <td>Hesaplanan KDV</td>
                            <td class="right"><xsl:value-of select="//cac:TaxTotal/cbc:TaxAmount"/></td>
                        </tr>
                        <tr>
                            <td>Vergiler Dahil Toplam Tutar</td>
                            <td class="right"><xsl:value-of select="//cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount"/></td>
                        </tr>
                        <tr>
                            <td class="bold">ÖDENECEK TUTAR</td>
                            <td class="bold right"><xsl:value-of select="//cac:LegalMonetaryTotal/cbc:PayableAmount"/> <xsl:value-of select="//cbc:DocumentCurrencyCode"/></td>
                        </tr>
                    </table>
                    <div class="clear"></div>
                    
                    <div style="margin-top: 30px; font-size: 11px; color: #555;">
                        <p><strong>Notlar:</strong> <xsl:value-of select="//cbc:Note"/></p>
                        <p><em>* Bu belge, tasarımsız e-Fatura/e-Arşiv XML verilerinden sistem tarafından otomatik üretilmiştir.</em></p>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>