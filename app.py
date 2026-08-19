import streamlit as st
import pandas as pd
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
import io

st.set_page_config(page_title="Cetak Label 15x30x2", layout="centered")
st.title("🏷️ Cetak Label 15x30 mm (2 Line)")

# Upload File Excel
uploaded_file = st.file_uploader("Upload File Excel Produk Anda", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("📋 **Preview Data Excel:**", df.head())

    st.sidebar.header("⚙️ Pengaturan Layout")
    font_size = st.sidebar.slider("Ukuran Font Teks", 4, 10, 6)
    gap_between = st.sidebar.slider("Jarak Antar Stiker (mm)", 0, 5, 2) * mm

    if st.button("🚀 Generate PDF Label"):
        buffer = io.BytesIO()

        # Dimensi 1 stiker: Lebar 30mm, Tinggi 15mm
        label_w = 30 * mm
        label_h = 15 * mm

        # Total lebar halaman = 2 label + gap
        page_w = (label_w * 2) + gap_between
        page_h = label_h

        pdf = canvas.Canvas(buffer, pagesize=(page_w, page_h))

        # Process data 2 per 2 (2 Line)
        for i in range(0, len(df), 2):
            for col in range(2):
                if i + col < len(df):
                    row = df.iloc[i + col]
                    nama = str(row.get('Nama_Produk', ''))
                    harga = str(row.get('Harga', ''))
                    sku = str(row.get('Barcode', ''))

                    x_offset = col * (label_w + gap_between)

                    # Tulis Nama Produk
                    pdf.setFont("Helvetica-Bold", font_size)
                    pdf.drawString(x_offset + 1*mm, label_h - 3.5*mm, nama[:14])

                    # Tulis Harga
                    pdf.setFont("Helvetica", max(font_size - 1, 4))
                    pdf.drawString(x_offset + 1*mm, label_h - 6.5*mm, f"Rp {harga}")

                    # Gambar Barcode
                    if sku:
                        try:
                            barcode = code128.Code128(sku, barHeight=4*mm, barWidth=0.3)
                            barcode.drawOn(pdf, x_offset + 1*mm, 1*mm)
                        except:
                            pass

            pdf.showPage()

        pdf.save()
        buffer.seek(0)

        st.success("✅ PDF Label 2-Line Siap Dicetak!")
        st.download_button(
            label="📥 Download PDF (2-Line)",
            data=buffer,
            file_name="label_15x30_2line.pdf",
            mime="application/pdf"
        )
