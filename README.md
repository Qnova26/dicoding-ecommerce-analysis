# E-Commerce Data Analysis Project

Proyek ini merupakan submission akhir untuk kelas "Belajar Analisis Data dengan Python" di **Dicoding**. Fokus utama dari proyek ini adalah melakukan analisis mendalam terhadap **E-Commerce Public Dataset** untuk mendapatkan wawasan bisnis yang strategis mengenai performa penjualan, kategori produk, dan perilaku pelanggan.

---

## Profil Pengembang
* **Nama:** Carlos Qnova Bha'a Gani
* **Pendidikan:** Teknologi Informasi, Universitas Udayana
* **Email:** carlosqnova88@gmail.com
* **Lokasi:** Denpasar, Bali

---

## Pertanyaan Bisnis
Proyek ini menjawab beberapa pertanyaan strategis berikut:
1. **Analisis Produk:** Kategori produk apa yang paling banyak terjual dan kategori mana yang menyumbang pendapatan (*revenue*) tertinggi?
2. **Tren Penjualan:** Bagaimana performa tren pesanan unik per bulan dalam rentang waktu operasional dataset?
3. **Analisis RFM:** Bagaimana segmentasi profil pelanggan berdasarkan parameter *Recency*, *Frequency*, dan *Monetary*?

---

## Tech Stack & Libraries
* **Python**: Bahasa pemrograman utama.
* **Pandas**: Digunakan untuk manipulasi dan pembersihan data (*Data Wrangling*).
* **Matplotlib & Seaborn**: Digunakan untuk visualisasi data yang statis dan informatif.
* **Streamlit**: Digunakan untuk membangun dashboard analisis yang interaktif.
* **Babel**: Digunakan untuk pemformatan mata uang dan angka yang akurat.

---

## Struktur Direktori
```text
.
├── dashboard/
│   ├── dashboard.py         # Kode utama aplikasi Streamlit
│   └── main_data.csv        # Dataset hasil pembersihan (digunakan oleh dashboard)
├── data/
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   └── ...                  # File dataset asli lainnya
├── notebook.ipynb           # Dokumentasi analisis lengkap dari awal hingga akhir
├── README.md                # Dokumentasi proyek (file ini)
├── requirements.txt         # Daftar pustaka (library) yang diperlukan
├── runtime.txt              # Konfigurasi versi Python untuk deployment
└── url.txt                  # Tautan live dashboard Streamlit Cloud