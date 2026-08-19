<!DOCTYPE html>
<html>
<head>
<style>
  @page {
    size: 15mm 30mm; /* Sesuaikan dengan ukuran fisik kertas label Anda */
    margin: 0;
  }
  body {
    width: 30mm;
    height: 15mm;
    margin: 0;
    padding: 1mm 2mm;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    overflow: hidden; /* Mencegah teks melimpah keluar label */
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
    text-overflow: ellipsis; /* Menambahkan '...' jika teks terlalu panjang */
    line-height: 1.1;
  }
  .barcode-container {
    width: 100%;
    text-align: center;
    margin: 1px 0;
  }
  .barcode-container img, .barcode-container svg {
    max-width: 100%;
    height: 9mm; /* Menjaga area barcode tetap bersih dari teks */
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

  <!-- Zona 1: Header & Nama Produk -->
  <div class="header">
    <div class="store-name">Pelangi AnR</div>
    <div class="product-name">Bando Sirkam Plastik</div>
  </div>

  <!-- Zona 2: Gambar Barcode Bersih -->
  <div class="barcode-container">
    <svg id="barcode"></svg>
  </div>

  <!-- Zona 3: Kode Produk & Harga -->
  <div class="footer">
    <span>AH030</span>
    <span>Rp 15.000</span>
  </div>

  <!-- Generasi Barcode Otomatis (menggunakan JsBarcode) -->
  <script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"></script>
  <script>
    JsBarcode("#barcode", "AH030", {
      format: "CODE128",
      displayValue: false, // Opsi penting: nonaktifkan teks bawaan barcode agar tidak bertumpuk
      margin: 0,
      height: 35
    });
  </script>
</body>
</html>
