# Analisis dan Pembersihan Data Tuna

Program ini dirancang untuk menganalisis dan membersihkan data perikanan tuna dari file Excel `tuna-fix.xlsx`. Program ini mengidentifikasi data kosong dan memperbaiki inkonsistensi antara satuan pounds dan metric tons.

## Fitur

1. **Analisis Struktur Data**: Menampilkan informasi dasar tentang dataset termasuk ukuran, kolom, tipe data, dan statistik deskriptif.
2. **Identifikasi Data Kosong**: Mengidentifikasi baris dengan data kosong di kolom penting (year, state, nmfs name, pounds, metric tons).
3. **Pembersihan Data**: Menghapus baris dengan data kosong di kolom kunci.
4. **Pemeriksaan Konsistensi**: Memeriksa konsistensi antara kolom pounds dan metric tons menggunakan konversi standar (1 metric ton = 2204.62 pounds).
5. **Perbaikan Data**: Memperbaiki data yang tidak konsisten dengan menggunakan konversi yang benar.
6. **Laporan Analisis**: Menghasilkan laporan lengkap tentang hasil analisis data.
7. **Visualisasi Data**: Membuat visualisasi untuk memahami hubungan antar variabel.
8. **Penyimpanan Data**: Menyimpan data yang sudah dibersihkan ke file Excel baru.

## Instalasi

Pastikan Anda telah menginstal Python 3.7 atau versi yang lebih baru. Kemudian instal dependensi yang diperlukan:

```bash
pip install -r requirements.txt
```

## Penggunaan

Untuk menjalankan analisis lengkap pada data tuna:

```bash
python analyze_tuna_data.py
```

Program akan secara otomatis:
1. Membaca file `tuna-fix.xlsx`
2. Menganalisis struktur data
3. Mengidentifikasi dan menghapus baris dengan data kosong
4. Memeriksa dan memperbaiki inkonsistensi antara pounds dan metric tons
5. Menghasilkan laporan analisis
6. Menyimpan data yang sudah dibersihkan ke `tuna_data_cleaned.xlsx`
7. Membuat visualisasi dan menyimpannya ke `tuna_data_visualization.png`

## Struktur Output

Setelah menjalankan program, Anda akan mendapatkan:

1. **Laporan Konsol**: Informasi detail tentang proses analisis di konsol
2. **Data Bersih**: File `tuna_data_cleaned.xlsx` berisi data yang sudah dibersihkan dan diperbaiki
3. **Visualisasi**: File `tuna_data_visualization.png` berisi grafik hubungan antar variabel

## Metodologi Pembersihan Data

### 1. Identifikasi Data Kosong
Program mengidentifikasi baris dengan data kosong di kolom-kolom berikut:
- year
- state
- nmfs name
- pounds
- metric tons

Baris dengan data kosong di salah satu kolom tersebut akan dihapus dari dataset.

### 2. Pemeriksaan Konsistensi
Program memeriksa konsistensi antara nilai pounds dan metric tons menggunakan konversi standar:
- 1 metric ton = 2204.62 pounds

Data dianggap tidak konsisten jika selisih antara nilai aktual dan nilai yang diharapkan melebihi toleransi 1%.

### 3. Perbaikan Data
Untuk data yang tidak konsisten, program menerapkan strategi perbaikan berikut:
- Jika kedua nilai ada, gunakan metric tons sebagai acuan (karena lebih presisi)
- Jika hanya metric tons yang ada, konversi ke pounds
- Jika hanya pounds yang ada, konversi ke metric tons

## Struktur Kelas

Program menggunakan kelas `TunaDataAnalyzer` dengan metode-metode berikut:
- `load_data()`: Memuat data dari file Excel
- `analyze_structure()`: Menganalisis struktur data
- `identify_empty_rows()`: Mengidentifikasi baris dengan data kosong
- `clean_data()`: Membersihkan data
- `check_consistency()`: Memeriksa konsistensi
- `fix_inconsistent_data()`: Memperbaiki data tidak konsisten
- `generate_report()`: Membuat laporan analisis
- `save_cleaned_data()`: Menyimpan data yang sudah dibersihkan
- `create_visualization()`: Membuat visualisasi data
- `run_full_analysis()`: Menjalankan seluruh proses analisis

## Contoh Output

```
=== MEMULAI ANALISIS DATA TUNA ===
Memuat data dari file Excel...
Data berhasil dimuat. Total baris: 10000

=== ANALISIS STRUKTUR DATA ===
Ukuran dataset: (10000, 9)
...

=== IDENTIFIKASI DATA KOSONG ===
Kolom penting yang diperiksa: ['year', 'state', 'nmfs name', 'pounds', 'metric tons']
Jumlah baris dengan data kosong di kolom penting: 150 (1.50%)

=== PEMBERSIHAN DATA ===
Total baris sebelum pembersihan: 10000
Total baris setelah pembersihan: 9850
Jumlah baris yang dihapus: 150

=== PEMERIKSAAN KONSISTENSI POUNDS VS METRIC TONS ===
Jumlah baris dengan data tidak konsisten: 200 (2.03%)

=== PERBAIKAN DATA TIDAK KONSISTEN ===
Memperbaiki 200 baris data tidak konsisten...
Perbaikan data selesai.
Memverifikasi kembali konsistensi data...
Jumlah baris yang masih tidak konsisten setelah perbaikan: 0

=== LAPORAN ANALISIS DATA TUNA ===
Tanggal pembuatan laporan: 2023-11-24 09:30:00

1. Ringkasan Dataset:
   - Total baris awal: 10000
   - Total baris setelah pembersihan: 9850
   - Persentase data yang tersimpan: 98.50%

...

Data yang sudah dibersihkan berhasil disimpan ke: tuna_data_cleaned.xlsx
Visualisasi berhasil disimpan ke: tuna_data_visualization.png

=== ANALISIS DATA SELESAI ===
```

## Kustomisasi

Anda dapat mengkustomisasi program dengan mengubah parameter berikut:
- `conversion_factor`: Faktor konversi antara metric tons dan pounds (default: 2204.62)
- `important_columns`: Daftar kolom penting yang tidak boleh kosong
- `tolerance`: Tingkat toleransi untuk pemeriksaan konsistensi (default: 1%)

## Troubleshooting

1. **Error saat membaca file Excel**: Pastikan file `tuna-fix.xlsx` ada di direktori yang sama dengan program.
2. **Error saat menyimpan file**: Pastikan Anda memiliki izin menulis di direktori tersebut.
3. **Import error**: Pastikan semua dependensi telah terinstal dengan benar menggunakan `pip install -r requirements.txt`.

## Lisensi

Program ini dirilis di bawah lisensi MIT.