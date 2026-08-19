import streamlit as st
import streamlit.components.v1 as components

# Pengaturan halaman Streamlit
st.set_page_config(page_title="Cetak Label Pelangi AnR", layout="wide")

st.title("Aplikasi Cetak Label Barcode")

# Sidebar untuk Input Data
st.sidebar.header("Data Label")
nama_toko = st.sidebar.text_input("Nama Toko", value="Pelangi AnR")
nama_produk = st.sidebar.text_input("Nama Produk", value="Bando Sirkam Plastik")
kode_produk = st.sidebar.text_input("Kode Produk / Barcode", value="AH030")
harga_produk = st.sidebar.text_input("Harga", value="15.000")
jumlah_kolom = st.sidebar.radio("Jumlah Label per Baris", [1, 3], index=1)

# Template HTML & CSS untuk Label
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @media print {{
    @page {{
      size: auto;
      margin: 0mm;
    }}
    body {{
      margin: 0;
      padding: 0;
    }}
    .no-print {{
      display: none !important;
    }}
  }}

  body {{
    font-family: Arial, sans-serif;
    margin: 10px;
  }}

  .label-container {{
    display: flex;
    gap: 2mm;
  }}

  .label-card {{
    width: 38mm;
    height: 19mm;
    border: 1px dashed #ccc; /* Garis bantu preview */
    padding: 1mm 1.5mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    background: #fff;
  }}

  /* Menghilangkan garis bantu saat dicetak */
  @media print {{
    .label-card {{
      border: none;
    }}
  }}

  .store-name {{
    font-size: 6.5pt;
    font-weight: bold;
    text-align: center;
    line-height: 1;
  }}

  .product-name {{
    font-size: 6pt;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 35mm;
    line-height: 1.1;
  }}

  .barcode-container {{
    width: 100%;
    text-align: center;
    margin: 0.5mm 0;
  }}

  .barcode-container svg {{
    max-width: 100%;
    height: 8mm;
    display: block;
    margin: 0 auto;
  }}

  .footer {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 6.5pt;
    font-weight: bold;
  }}

  .btn-print {{
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    margin-bottom: 15px;
  }}
</style>
</head>
<body>

  <button class="btn-print no-print" onclick="window.print()">🖨️ Cetak Label</button>

  <div class="label-container">
"""

# Menambahkan jumlah label sesuai pilihan (1 atau 3 kolom)
for i in range(jumlah_kolom):
    html_code += f"""
    <div class="label-card">
      <div>
        <div class="store-name">{nama_toko}</div>
        <div class="product-name">{nama_produk}</div>
      </div>
      <div class="barcode-container">
        <svg id="barcode-{i}"></svg>
      </div>
      <div class="footer">
        <span>{kode_produk}</span>
        <span>Rp {harga_produk}</span>
      </div>
    </div>
    """

html_code += f"""
  </div>

  <script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"></script>
  <script>
    for (let i = 0; i < {jumlah_kolom}; i++) {{
      JsBarcode("#barcode-" + i, "{kode_produk}", {{
        format: "CODE128",
        displayValue: false,
        margin: 0,
        height: 30
      }});
    }}
  </script>
</body>
</html>
"""

# Render komponen HTML di Streamlit
components.html(html_code, height=200, scrolling=True)
