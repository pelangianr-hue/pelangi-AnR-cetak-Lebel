import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Pengaturan halaman Streamlit
st.set_page_config(page_title="Cetak Label Pelangi AnR", layout="wide")

st.title("Aplikasi Cetak Label Barcode - Bulk Print")

# Sidebar - Mode Input Data
st.sidebar.header("Pengaturan Cetak")
mode_input = st.sidebar.radio("Sumber Data", ["Input Manual", "Upload Excel"])

nama_toko_default = st.sidebar.text_input("Nama Toko Default", value="Pelangi AnR")
jumlah_kolom = st.sidebar.radio("Pilih Jumlah Label per Baris", [1, 2, 3], index=1)

items = []

if mode_input == "Input Manual":
    st.sidebar.subheader("Data Single Item")
    nama_produk = st.sidebar.text_input("Nama Produk", value="Bando Sirkam Plastik")
    kode_produk = st.sidebar.text_input("Kode Produk / Barcode", value="AH030")
    harga_produk = st.sidebar.text_input("Harga", value="15.000")
    jumlah_cetak = st.sidebar.number_input("Jumlah Cetak Label", min_value=1, value=1)
    
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
    
    st.sidebar.info("""
    **Format Kolom Excel:**
    * `nama_produk`
    * `kode_produk`
    * `harga`
    * `jumlah` (Opsional, default 1)
    """)

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("---")
            st.subheader("Preview Data Excel:")
            st.dataframe(df)

            for index, row in df.iterrows():
                # Membaca kolom excel
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

# Render Komponen Cetak
if items:
    # Membangun HTML Label
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

      .label-grid {{
        display: grid;
        grid-template-columns: repeat({jumlah_kolom}, 38mm);
        gap: 3mm 2mm;
        justify-content: start;
      }}

      .label-card {{
        width: 38mm;
        height: 19mm;
        border: 1px dashed #ccc;
        padding: 1mm 1.5mm;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        background: #fff;
        page-break-inside: avoid;
      }}

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

      <button class="btn-print no-print" onclick="window.print()">🖨️ Cetak Semua Label ({len(items)} Label)</button>

      <div class="label-grid">
    """

    # Loop seluruh item untuk dibuatkan card labelnya
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
            <span>{item['kode']}</span>
            <span>Rp {item['harga']}</span>
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

    # Hitung tinggi container preview secara dinamis
    total_rows = (len(items) + jumlah_kolom - 1) // jumlah_kolom
    dynamic_height = max(250, total_rows * 90)

    components.html(html_code, height=dynamic_height, scrolling=True)

else:
    st.info("Silakan masukkan data secara manual atau upload file Excel untuk menampilkan preview cetak.")
