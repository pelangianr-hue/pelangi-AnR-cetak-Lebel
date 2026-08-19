import streamlit as st
import pandas as pd
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128, eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
import io

st.set_page_config(page_title="Print Label Pro - pelangi AnR Style", page_icon="🏷️", layout="wide")

# CSS Styling untuk Tampilan Mirip OpenLabel
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    .label-card {
        border: 1px dashed #777;
        background-color: #ffffff;
        padding: 8px;
        width: 100%;
        min-height: 120px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        font-family: Arial, sans-serif;
    }
    .store-name { font-size: 11px; font-weight: bold; text-align: left; margin: 0; }
    .prod-name { font-size: 10px; line-height: 1.1; margin-top: 2px; text-align: left; }
    .price-tag { font-size: 16px; font-weight: bold; text-align: right; margin-top: 4px; }
    .sku-tag { font-size: 9px; text-align: center; margin-top: 2px; font-weight: bold; }
    .barcode-mock { text-align: center; font-size: 18px; letter-spacing: -1px; margin-top: -5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏷️ Studio Label Toko (2 Line - 15x30 mm)")

# Inisialisasi Tab
tab_data, tab_custom, tab_preview, tab_print = st.tabs([
    "📂 1. Data Excel", 
    "⚙️ 2. Tab Kustomisasi", 
    "👁️ 3. Live Preview", 
    "🖨️ 4. Cetak PDF"
])

# --- TAB 1: DATA EXCEL ---
with tab_data:
    st.subheader("Upload & Pilih Data Produk")
    uploaded_file = st.file_uploader("Upload File Excel (.xlsx / .xls)", type=["xlsx", "xls"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if "Pilih" not in df.columns:
            df.insert(0, "Pilih", True)
        if "Jumlah_Cetak" not in df.columns:
            df.insert(1, "Jumlah_Cetak", 1)
            
        edited_df = st.data_editor(
            df,
            column_config={
                "Pilih": st.column_config.CheckboxColumn("Cetak?", default=True),
                "Jumlah_Cetak": st.column_config.NumberColumn("Jml Stiker", min_value=1, max_value=100, default=1)
            },
            disabled=[col for col in df.columns if col not in ["Pilih", "Jumlah_Cetak"]],
            use_container_width=True,
            hide_index=True
        )
        selected_df = edited_df[edited_df["Pilih"] == True]
        st.success(f" Total {len(selected_df)} jenis produk terpilih.")

# --- TAB 2: TAB KUSTOMISASI ---
with tab_custom:
    st.subheader(" ⚙️ Pengaturan Layout & Elemen Label")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        st.markdown("**1. Informasi Toko & Teks**")
        store_name = st.text_input("Nama Toko Header", value="pelangi AnR")
        show_store = st.checkbox("Tampilkan Nama Toko", value=True)
        show_name = st.checkbox("Tampilkan Nama Produk", value=True)
        show_price = st.checkbox("Tampilkan Harga", value=True)
        show_sku_text = st.checkbox("Tampilkan Kode SKU di atas Barcode", value=True)
        
    with col_c2:
        st.markdown("**2. Format & Tipe Barcode**")
        barcode_type = st.selectbox("Jenis Barcode", ["Code 128 (Umum)", "EAN-13 (Standard Retail 13 Digit)"])
        show_barcode = st.checkbox("Tampilkan Gambar Barcode", value=True)
        barcode_height_mm = st.slider("Tinggi Barcode (mm)", 2, 6, 4)
        
    with col_c3:
        st.markdown("**3. Pemetaan Kolom Excel**")
        if uploaded_file:
            cols = list(df.columns)
            col_prod = st.selectbox("Kolom Nama Produk", options=cols, index=cols.index("Nama_Produk") if "Nama_Produk" in cols else 0)
            col_price = st.selectbox("Kolom Harga", options=cols, index=cols.index("Harga") if "Harga" in cols else 0)
            col_code = st.selectbox("Kolom Barcode/SKU", options=cols, index=cols.index("Barcode") if "Barcode" in cols else 0)
        else:
            col_prod, col_price, col_code = "Nama_Produk", "Harga", "Barcode"

# --- TAB 3: LIVE PREVIEW ---
with tab_preview:
    st.subheader("👁️ Simulasi Tampilan Hasil Jadi")
    
    if uploaded_file and len(selected_df) > 0:
        sample = selected_df.iloc[0]
        p_name = str(sample.get(col_prod, "Botol Spray 35ml"))
        p_price = str(sample.get(col_price, "7.500"))
        p_code = str(sample.get(col_code, "F039"))
        
        col_pv1, col_pv2 = st.columns(2)
        for pv, label_title in zip([col_pv1, col_pv2], ["Stiker Kiri (Line 1)", "Stiker Kanan (Line 2)"]):
            with pv:
                st.caption(label_title)
                st.markdown(f"""
                <div class="label-card">
                    {f'<div class="store-name">{store_name}</div>' if show_store else ''}
                    {f'<div class="prod-name">{p_name}</div>' if show_name else ''}
                    {f'<div class="price-tag">Rp {p_price}</div>' if show_price else ''}
                    {f'<div class="sku-tag">{p_code}</div>' if show_sku_text else ''}
                    {f'<div class="barcode-mock">|||||||||||||||||||||||||</div>' if show_barcode else ''}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Upload file Excel di Tab 1 untuk melihat preview interaktif.")

# --- TAB 4: CETAK PDF ---
with tab_print:
    st.subheader("🖨️ Export PDF Siap Cetak")
    
    if uploaded_file and len(selected_df) > 0:
        # Replikasi data sesuai Jumlah_Cetak
        expanded_rows = []
        for _, row in selected_df.iterrows():
            qty = int(row.get("Jumlah_Cetak", 1))
            for _ in range(qty):
                expanded_rows.append(row)
        print_df = pd.DataFrame(expanded_rows)
        
        st.write(f"Total Stiker yang akan Dicetak: **{len(print_df)} Pcs**")
        
        if st.button("🚀 GENERATE PDF (SIAP PRINT BLUEPRINT ECO80)"):
            buffer = io.BytesIO()
            label_w, label_h = 30 * mm, 15 * mm
            gap_between = 2 * mm
            page_w, page_h = (label_w * 2) + gap_between, label_h

            pdf = canvas.Canvas(buffer, pagesize=(page_w, page_h))

            for i in range(0, len(print_df), 2):
                for col in range(2):
                    if i + col < len(print_df):
                        row = print_df.iloc[i + col]
                        nama = str(row.get(col_prod, ''))
                        harga = str(row.get(col_price, ''))
                        sku = str(row.get(col_code, ''))

                        x_off = col * (label_w + gap_between)

                        # 1. Header Nama Toko
                        if show_store:
                            pdf.setFont("Helvetica-Bold", 4.5)
                            pdf.drawString(x_off + 1*mm, label_h - 2.5*mm, store_name)

                        # 2. Nama Produk (2 Baris)
                        if show_name:
                            pdf.setFont("Helvetica-Bold", 4.5)
                            pdf.drawString(x_off + 1*mm, label_h - 5*mm, nama[:15])
                            if len(nama) > 15:
                                pdf.drawString(x_off + 1*mm, label_h - 7*mm, nama[15:30])

                        # 3. Harga Produk (Kanan Bawah)
                        if show_price:
                            pdf.setFont("Helvetica-Bold", 7.5)
                            pdf.drawRightString(x_off + label_w - 1*mm, 5.5*mm, f"Rp {harga}")

                        # 4. SKU Code
                        if show_sku_text and sku:
                            pdf.setFont("Helvetica-Bold", 4)
                            pdf.drawCentredString(x_off + (label_w/2), 4.2*mm, sku)

                        # 5. Barcode
                        if show_barcode and sku:
                            try:
                                if "EAN-13" in barcode_type:
                                    clean_sku = ''.join(filter(str.isdigit, sku)).zfill(12)[:12]
                                    ean = eanbc.Ean13BarcodeWidget(clean_sku, barHeight=barcode_height_mm*mm, barWidth=0.2*mm)
                                    d = Drawing(20*mm, barcode_height_mm*mm)
                                    d.add(ean)
                                    renderPDF.draw(d, pdf, x_off + 3*mm, 0.5*mm)
                                else:
                                    bc = code128.Code128(sku, barHeight=barcode_height_mm*mm, barWidth=0.2)
                                    bc.drawOn(pdf, x_off + 3*mm, 0.5*mm)
                            except:
                                pass
                pdf.showPage()

            pdf.save()
            buffer.seek(0)

            st.download_button(
                label="📥 UNDUH FILE PDF LABEL",
                data=buffer,
                file_name="Label_pelangi_AnR.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Silakan tuntaskan pengaturan data di Tab 1 terlebih dahulu.")
