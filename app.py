import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Pengaturan halaman Streamlit
st.set_page_config(page_title="Cetak Label Pelangi AnR - GAP 2 Line", layout="wide")

st.title("Aplikasi Cetak Label Barcode - Label GAP 2 Line")

# ==================== SIDEBAR ====================
st.sidebar.header("1. Pengaturan Data")
mode_input = st.sidebar.radio("Sumber Data", ["Input Manual", "Upload Excel"])

nama_toko_default = st.sidebar.text_input("Nama Toko Default", value="Pelangi AnR")

# Setting khusus kertas GAP 2 Line
jumlah_kolom = 2  

# --- CONTROL PANEL LAYOUT (Pengaturan Ukuran) ---
st.sidebar.header("2. Ukuran Label GAP (mm)")
lebar_label = st.sidebar.number_input("Lebar 1 Label (mm)", value=38)
tinggi_label = st.sidebar.number_input("Tinggi 1 Label (mm)", value=20)
gap_horizontal = st.sidebar.number_input("Jarak GAP Tengah (mm)", value=2)

st.sidebar.header("3. Pengaturan Teks & Barcode")
ukuran_harga = st.sidebar.slider("Ukuran Teks Harga (pt)", min_value=5, max_value=14, value=8)
ukuran_kode = st.sidebar.slider("Ukuran Teks Kode (pt)", min_value=5, max_value=12, value=7)
ukuran_nama = st.sidebar.slider("Ukuran Nama Produk (pt)", min_value=5, max_value=12, value=6)
ukuran_toko = st.sidebar.slider("Ukuran Teks Toko (pt)", min_value=5, max_value=12, value=7)
tinggi_barcode = st.sidebar.slider("Tinggi Barcode (mm)", min_value=4, max_value=15, value=8)

# ==================== PENGOLAHAN DATA ====================
items = []

if mode_input == "Input Manual":
    st.sidebar.subheader("Data Single Item")
    nama_produk = st.sidebar.text_input("Nama Produk", value="Bando Sirkam Plastik")
    kode_produk = st.sidebar.text_input("Kode Produk / Barcode", value="AH030")
    harga_produk = st.sidebar.text_input("Harga", value="15.000")
    jumlah_cetak = st.sidebar.number_input("Jumlah Cetak Label", min_value=1, value=2)
    
    for _ in range(jumlah_cetak):
        items.append({
            "toko": nama_toko_default,
            "nama": nama_produk,
            "kode": kode_produk,
            "harga": harga_produk
        })

else:
    st.sidebar.subheader("Upload File Excel")
    uploaded_file = st.sidebar.file_uploader("Pilih File Excel (.xlsx / .xls)", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("---")
            st.subheader("Preview Data Excel:")
            st.dataframe(df)

            for index, row in df.iterrows():
                nama_p = str(row.get('nama_produk', ''))
                kode_p = str(row.get('kode_produk', ''))
                harga_p = str(row.get('harga', ''))
                qty = int(row.get('jumlah', 1))

                for _ in range(qty):
                    items.append({
                        "toko": nama_toko_default,
                        "nama": nama_p,
                        "kode": kode_p,
                        "harga": harga_p
                    })
        except Exception as e:
            st.error(f"Gagal membaca file Excel: {e}")

# ==================== RENDER LABEL ====================
if items:
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      @media print {{
        @page {{
          size: auto;
          margin: 0mm;
        }}
        body {{
          margin: 0;
          padding: 0;
          background: #fff;
        }}
        .no-print {{
          display: none !important;
        }}
        .label-card {{
          border: none !important;
        }}
      }}

      body {{
        font-family: Arial, sans-serif;
        margin: 10px;
        background: #f4f4f4;
      }}

      .label-grid {{
        display: grid;
        grid-template-columns: repeat(2, {lebar_label}mm);
        gap: 3mm {gap_horizontal}mm;
        justify-content: start;
      }}

      .label-card {{
        width: {lebar_label}mm;
        height: {tinggi_label}mm;
        border: 1px dashed #bbb;
        padding: 1mm 1.5mm;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        background: #fff;
        page-break-inside: avoid;
        overflow: hidden;
      }}

      .store-name {{
        font-size: {ukuran_toko}pt;
        font-weight: bold;
        text-align: center;
        line-height: 1;
      }}

      .product-name {{
        font-size: {ukuran_nama}pt;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: {lebar_label - 3}mm;
        line-height: 1.1;
      }}

      .barcode-container {{
        width: 100%;
        text-align: center;
        margin: 0.5mm 0;
      }}

      .barcode-container svg {{
        max-width: 100%;
        height: {tinggi_barcode}mm;
        display: block;
        margin: 0 auto;
      }}

      .footer {{
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        line-height: 1;
      }}

      .text-kode {{
        font-size: {ukuran_kode}pt;
        font-weight: bold;
      }}

      .text-harga {{
        font-size: {ukuran_harga}pt;
        font-weight: bold;
      }}

      .btn-print {{
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 15px;
        margin-bottom: 15px;
        font-weight: bold;
      }}
    </style>
    </head>
    <body>

      <button class="btn-print no-print" onclick="window.print()">🖨️ Cetak ke Thermal Printer ({len(items)} Label)</button>

      <div class="label-grid">
    """

    for idx, item in enumerate(items):
        html_code += f"""
        <div class="label-card">
          <div>
            <div class="store-name">{item['toko']}</div>
            <div class="product-name">{item['nama']}</div>
          </div>
          <div class="barcode-container">
            <svg id="barcode-{idx}"></svg>
          </div>
          <div class="footer">
            <span class="text-kode">{item['kode']}</span>
            <span class="text-harga">Rp {item['harga']}</span>
          </div>
        </div>
        """

    html_code += f"""
      </div>

      <script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"></script>
      <script>
        const itemData = {[{ "id": f"barcode-{i}", "code": item['kode']} for i, item in enumerate(items)]};
        
        itemData.forEach(item => {{
          try {{
            JsBarcode("#" + item.id, item.code, {{
              format: "CODE128",
              displayValue: false,
              margin: 0,
              height: 30
            }});
          }} catch(e) {{
            console.error(e);
          }}
        }});
      </script>
    </body>
    </html>
    """

    st.download_button(
        label="📥 Download Format File Cetak (HTML)",
        data=html_code,
        file_name="cetak_label_gap2line.html",
        mime="text/html"
    )

    total_rows = (len(items) + 1) // 2
    dynamic_height = max(250, total_rows * 90)

    components.html(html_code, height=dynamic_height, scrolling=True)

else:
    st.info("Silakan masukkan data secara manual atau upload file Excel untuk menampilkan preview cetak.")
