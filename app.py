import streamlit as st
import pandas as pd
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128, eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
import io

st.set_page_config(page_title="Cetak Label OpenLabel Style", page_icon="🏷️", layout="wide")

# CSS Kustom untuk Tampilan Mirip OpenLabel
st.markdown("""
    <style>
    .preview-card {
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 8px;
        background-color: #ffffff;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏷️ Pembuat Label Toko (OpenLabel Style)")
st.caption("Khusus Stiker 15x30 mm (2 Line) / Bluetooth Thermal ECO80")

# 1. UPLOAD FILE EXCEL
uploaded_file = st.file_uploader("📂 Upload File Excel Data Produk Anda", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # KEBUTUHAN 4: SOROT DATA / BARIS DARI EXCEL
    st.subheader("📊 1. Sorot & Pilih Data yang Akan Dicetak")
    
    # Tambahkan kolom centang secara interaktif
    df.insert(0, "Cetak", True)
    edited_df = st.data_editor(
        df,
        column_config={"Cetak": st.column_config.CheckboxColumn("Pilih", default=True)},
        disabled=[col for col in df.columns if col != "Cetak"],
        hide_index=True,
        use_container_width=True
    )
    
    # Filter hanya data yang dicentang user
    selected_data = edited_df[edited_df["Cetak"] == True].drop(columns=["Cetak"])
    
    if len(selected_data) == 0:
        st.warning("⚠️ Silakan centang minimal 1 data produk untuk dicetak.")
    else:
        st.success(f"✅ Total {len(selected_data)} item dipilih.")

        # KEBUTUHAN 2 & 3: KUSTOMISASI ELEMEN & TIPE BARCODE
        st.subheader("⚙️ 2. Kustomisasi Isi & Format Barcode")
        col_opt1, col_opt2 = st.columns(2)
        
        with col_opt1:
            st.markdown("**Format Barcode:**")
            barcode_type = st.radio(
                "Pilih Jenis Barcode:",
                ["Code 128 (Angka & Huruf)", "EAN-13 (13 Digit Angka Murni)"],
                horizontal=True
            )
            
        with col_opt2:
            st.markdown("**Item yang Ditampilkan di Label:**")
            show_nama = st.checkbox("Nama Produk", value=True)
            show_harga = st.checkbox("Harga Produk", value=True)
            show_barcode_img = st.checkbox("Gambar Barcode", value=True)
            show_sku_text = st.checkbox("Teks Kode Barcode / SKU", value=True)

        # KEBUTUHAN 1: JENDELA PREVIEW
        st.subheader("👁️ 3. Preview Hasil Jadi Label (15x30 mm)")
        
        sample_item = selected_data.iloc[0]
        s_nama = str(sample_item.get('Nama_Produk', 'Nama Produk'))[:14] if show_nama else ""
        s_harga = f"Rp {sample_item.get('Harga', '0')}" if show_harga else ""
        s_code = str(sample_item.get('Barcode', '123456789012')) if show_sku_text else ""

        col_p1, col_p2 = st.columns(2)
        for p_col, title in zip([col_p1, col_p2], ["Stiker Kiri (Line 1)", "Stiker Kanan (Line 2)"]):
            with p_col:
                st.caption(title)
                preview_html = f"<div class='preview-card'>"
                if show_nama: preview_html += f"<b>{s_nama}</b><br>"
                if show_harga: preview_html += f"<span style='color:red; font-weight:bold;'>{s_harga}</span><br>"
                if show_barcode_img: preview_html += "<small>|||||||||||||||||||||</small><br>"
                if show_sku_text: preview_html += f"<small>{s_code}</small>"
                preview_html += "</div>"
                st.markdown(preview_html, unsafe_allow_html=True)

        # GENERATE PDF SIAP PRINT
        if st.button("🚀 CETAK / DOWNLOAD FILE PDF"):
            buffer = io.BytesIO()
            label_w, label_h = 30 * mm, 15 * mm
            gap_between = 2 * mm
            page_w, page_h = (label_w * 2) + gap_between, label_h

            pdf = canvas.Canvas(buffer, pagesize=(page_w, page_h))

            for i in range(0, len(selected_data), 2):
                for col in range(2):
                    if i + col < len(selected_data):
                        row = selected_data.iloc[i + col]
                        nama = str(row.get('Nama_Produk', ''))
                        harga = str(row.get('Harga', ''))
                        sku = str(row.get('Barcode', ''))

                        x_offset = col * (label_w + gap_between)

                        # Draw Nama
                        if show_nama:
                            pdf.setFont("Helvetica-Bold", 6)
                            pdf.drawString(x_offset + 1*mm, label_h - 3.5*mm, nama[:14])

                        # Draw Harga
                        if show_harga:
                            pdf.setFont("Helvetica", 5)
                            pdf.drawString(x_offset + 1*mm, label_h - 6.5*mm, f"Rp {harga}")

                        # Draw Barcode (EAN-13 / Code128)
                        if show_barcode_img and sku:
                            try:
                                if "EAN-13" in barcode_type:
                                    # EAN13 butuh 12/13 digit angka
                                    clean_sku = ''.join(filter(str.isdigit, sku)).zfill(12)[:12]
                                    ean = eanbc.Ean13BarcodeWidget(clean_sku, barHeight=4*mm, barWidth=0.25*mm)
                                    d = Drawing(25*mm, 4*mm)
                                    d.add(ean)
                                    renderPDF.draw(d, pdf, x_offset + 1*mm, 1.5*mm)
                                else:
                                    # Code 128
                                    bc = code128.Code128(sku, barHeight=3.5*mm, barWidth=0.25)
                                    bc.drawOn(pdf, x_offset + 1*mm, 1.5*mm)
                            except:
                                pass

                pdf.showPage()

            pdf.save()
            buffer.seek(0)

            st.download_button(
                label="📥 UNDUH PDF LABEL (SIAP PRINT VIA RAWBT)",
                data=buffer,
                file_name="label_openlabel_style.pdf",
                mime="application/pdf"
            )
