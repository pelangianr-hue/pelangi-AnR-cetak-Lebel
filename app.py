import streamlit as st
import streamlit.components.v1 as components

st.title("Aplikasi Cetak Label")

# Bungkus kode HTML & CSS ke dalam string multiline (menggunakan triple quotes)
html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
  @page {
    size: 40mm 20mm;
    margin: 0;
  }
  body {
    width: 40mm;
    height: 20mm;
    margin: 0;
    padding: 1mm 2mm;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    overflow: hidden;
  }
  .header {
    width: 100%;
    text-align: center;
  }
  .store-name {
    font-size: 7pt;
    font-weight: bold;
    white-space: nowrap;
  }
  .product-name {
    font-size: 6.5pt;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.1;
  }
  .barcode-container {
    width: 100%;
    text-align: center;
    margin: 1px 0;
  }
  .barcode-container svg {
    max-width: 100%;
    height: 9mm;
    display: block;
    margin: 0 auto;
  }
  .footer {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7pt;
    font-weight: bold;
  }
</style>
</head>
<body>

  <div class="header">
    <div class="store-name">Pelangi AnR</div>
    <div class="product-name">Bando Sirkam Plastik</div>
  </div>

  <div class="barcode-container">
    <svg id="barcode"></svg>
  </div>

  <div class="footer">
    <span>AH030</span>
    <span>Rp 15.000</span>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"></script>
  <script>
    JsBarcode("#barcode", "AH030", {
      format: "CODE128",
      displayValue: false,
      margin: 0,
      height: 35
    });
  </script>
</body>
</html>
"""

# Tampilkan HTML di Streamlit
components.html(html_code, height=150)
