import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

class TunaDataAnalyzer:
    def __init__(self, file_path):
        """
        Inisialisasi analyzer dengan path ke file Excel
        """
        self.file_path = file_path
        self.original_data = None
        self.cleaned_data = None
        self.conversion_factor = 2204.62  # 1 metric ton = 2204.62 pounds
        
    def load_data(self):
        """
        Memuat data dari file Excel
        """
        try:
            print("Memuat data dari file Excel...")
            self.original_data = pd.read_excel(self.file_path)
            print(f"Data berhasil dimuat. Total baris: {len(self.original_data)}")
            return True
        except Exception as e:
            print(f"Error saat memuat data: {str(e)}")
            return False
    
    def analyze_structure(self):
        """
        Menganalisis struktur data dan menampilkan informasi dasar
        """
        if self.original_data is None:
            print("Data belum dimuat. Jalankan load_data() terlebih dahulu.")
            return
            
        print("\n=== ANALISIS STRUKTUR DATA ===")
        print(f"Ukuran dataset: {self.original_data.shape}")
        print(f"\nKolom-kolom yang ada:")
        for i, col in enumerate(self.original_data.columns):
            print(f"{i+1}. {col}")
        
        print(f"\nTipe data setiap kolom:")
        print(self.original_data.dtypes)
        
        print(f"\nStatistik deskriptif untuk kolom numerik:")
        print(self.original_data.describe())
        
        # Memeriksa missing values
        print(f"\nJumlah missing values per kolom:")
        missing_values = self.original_data.isnull().sum()
        for col, count in missing_values.items():
            percentage = (count / len(self.original_data)) * 100
            print(f"{col}: {count} ({percentage:.2f}%)")
    
    def identify_empty_rows(self):
        """
        Mengidentifikasi baris dengan data kosong di kolom penting
        """
        if self.original_data is None:
            print("Data belum dimuat. Jalankan load_data() terlebih dahulu.")
            return None
            
        # Kolom-kolom penting yang tidak boleh kosong (case-insensitive)
        important_columns_lower = ['year', 'state', 'nmfs name', 'pounds', 'metric tons']
        
        # Mencocokkan kolom dengan case yang ada di dataset
        available_columns = []
        for col in important_columns_lower:
            # Cari kolom yang cocok (case-insensitive)
            matching_cols = [data_col for data_col in self.original_data.columns if data_col.lower() == col.lower()]
            if matching_cols:
                available_columns.append(matching_cols[0])  # Gunakan yang pertama yang cocok
        
        missing_columns = [col for col in important_columns_lower if not any(data_col.lower() == col.lower() for data_col in self.original_data.columns)]
        
        if missing_columns:
            print(f"Peringatan: Kolom berikut tidak ditemukan dalam dataset: {missing_columns}")
        
        print(f"\n=== IDENTIFIKASI DATA KOSONG ===")
        print(f"Kolom penting yang diperiksa: {available_columns}")
        
        # Mengidentifikasi baris dengan data kosong
        empty_rows = self.original_data[available_columns].isnull().any(axis=1)
        empty_count = empty_rows.sum()
        
        print(f"Jumlah baris dengan data kosong di kolom penting: {empty_count} ({(empty_count/len(self.original_data))*100:.2f}%)")
        
        return empty_rows
    
    def clean_data(self):
        """
        Membersihkan data dengan menghapus baris yang memiliki data kosong di kolom penting
        """
        if self.original_data is None:
            print("Data belum dimuat. Jalankan load_data() terlebih dahulu.")
            return False
            
        # Kolom-kolom penting yang tidak boleh kosong (case-insensitive)
        important_columns_lower = ['year', 'state', 'nmfs name', 'pounds', 'metric tons']
        
        # Mencocokkan kolom dengan case yang ada di dataset
        available_columns = []
        for col in important_columns_lower:
            # Cari kolom yang cocok (case-insensitive)
            matching_cols = [data_col for data_col in self.original_data.columns if data_col.lower() == col.lower()]
            if matching_cols:
                available_columns.append(matching_cols[0])  # Gunakan yang pertama yang cocok
        
        print(f"\n=== PEMBERSIHAN DATA ===")
        print(f"Total baris sebelum pembersihan: {len(self.original_data)}")
        
        # Menghapus baris dengan data kosong di kolom penting
        self.cleaned_data = self.original_data.dropna(subset=available_columns).copy()
        
        print(f"Total baris setelah pembersihan: {len(self.cleaned_data)}")
        print(f"Jumlah baris yang dihapus: {len(self.original_data) - len(self.cleaned_data)}")
        
        return True
    
    def check_consistency(self):
        """
        Memeriksa konsistensi antara kolom pounds dan metric tons
        """
        if self.cleaned_data is None:
            print("Data belum dibersihkan. Jalankan clean_data() terlebih dahulu.")
            return None
            
        print(f"\n=== PEMERIKSAAN KONSISTENSI POUNDS VS METRIC TONS ===")
        
        # Mencari kolom pounds dan metric tons (case-insensitive)
        pounds_col = None
        metric_tons_col = None
        
        for col in self.cleaned_data.columns:
            if col.lower() == 'pounds':
                pounds_col = col
            elif col.lower() == 'metric tons':
                metric_tons_col = col
        
        if pounds_col is None or metric_tons_col is None:
            print(f"Kolom 'pounds' ({pounds_col}) atau 'metric tons' ({metric_tons_col}) tidak ditemukan dalam data.")
            print(f"Kolom yang tersedia: {list(self.cleaned_data.columns)}")
            return None
        
        # Konversi kolom ke numerik jika belum
        self.cleaned_data[pounds_col] = pd.to_numeric(self.cleaned_data[pounds_col], errors='coerce')
        self.cleaned_data[metric_tons_col] = pd.to_numeric(self.cleaned_data[metric_tons_col], errors='coerce')
        
        # Menghapus baris dengan nilai NaN setelah konversi
        self.cleaned_data = self.cleaned_data.dropna(subset=[pounds_col, metric_tons_col])
        
        # Menghitung konversi yang diharapkan
        expected_pounds = self.cleaned_data[metric_tons_col] * self.conversion_factor
        expected_metric_tons = self.cleaned_data[pounds_col] / self.conversion_factor
        
        # Menghitung selisih
        diff_pounds = abs(self.cleaned_data[pounds_col] - expected_pounds)
        diff_metric_tons = abs(self.cleaned_data[metric_tons_col] - expected_metric_tons)
        
        # Mengidentifikasi data tidak konsisten (dengan toleransi 1%)
        tolerance_pounds = 0.01 * self.cleaned_data[pounds_col]
        tolerance_metric_tons = 0.01 * self.cleaned_data[metric_tons_col]
        
        inconsistent_pounds = diff_pounds > tolerance_pounds
        inconsistent_metric_tons = diff_metric_tons > tolerance_metric_tons
        inconsistent_rows = inconsistent_pounds | inconsistent_metric_tons
        
        inconsistent_count = inconsistent_rows.sum()
        print(f"Jumlah baris dengan data tidak konsisten: {inconsistent_count} ({(inconsistent_count/len(self.cleaned_data))*100:.2f}%)")
        
        # Menampilkan beberapa contoh data tidak konsisten
        if inconsistent_count > 0:
            print(f"\nContoh data tidak konsisten (5 pertama):")
            inconsistent_data = self.cleaned_data[inconsistent_rows].head()
            for idx, row in inconsistent_data.iterrows():
                actual_conversion = row[pounds_col] / row[metric_tons_col] if row[metric_tons_col] != 0 else 0
                print(f"Baris {idx}: {row[pounds_col]} pounds vs {row[metric_tons_col]} metric tons (konversi aktual: {actual_conversion:.2f})")
        
        return inconsistent_rows
    
    def fix_inconsistent_data(self, inconsistent_rows):
        """
        Memperbaiki data yang tidak konsisten
        """
        if self.cleaned_data is None or inconsistent_rows is None:
            print("Data belum dianalisis. Jalankan check_consistency() terlebih dahulu.")
            return False
            
        print(f"\n=== PERBAIKAN DATA TIDAK KONSISTEN ===")
        
        # Membuat salinan data untuk perbaikan
        fixed_data = self.cleaned_data.copy()
        
        # Mencari kolom pounds dan metric tons (case-insensitive)
        pounds_col = None
        metric_tons_col = None
        
        for col in fixed_data.columns:
            if col.lower() == 'pounds':
                pounds_col = col
            elif col.lower() == 'metric tons':
                metric_tons_col = col
        
        # Mengidentifikasi baris yang tidak konsisten
        inconsistent_indices = fixed_data[inconsistent_rows].index
        
        print(f"Memperbaiki {len(inconsistent_indices)} baris data tidak konsisten...")
        
        # Strategi perbaikan:
        # 1. Jika kedua nilai ada, gunakan metric tons sebagai acuan (karena lebih presisi)
        # 2. Jika hanya salah satu yang ada, konversi dari yang ada
        
        for idx in inconsistent_indices:
            row = fixed_data.loc[idx]
            
            # Jika kedua nilai ada dan tidak nol
            if pd.notna(row[pounds_col]) and pd.notna(row[metric_tons_col]) and row[metric_tons_col] > 0:
                # Gunakan metric tons sebagai acuan dan hitung ulang pounds
                fixed_data.loc[idx, pounds_col] = row[metric_tons_col] * self.conversion_factor
            elif pd.notna(row[metric_tons_col]) and row[metric_tons_col] > 0:
                # Hanya metric tons yang ada, konversi ke pounds
                fixed_data.loc[idx, pounds_col] = row[metric_tons_col] * self.conversion_factor
            elif pd.notna(row[pounds_col]) and row[pounds_col] > 0:
                # Hanya pounds yang ada, konversi ke metric tons
                fixed_data.loc[idx, metric_tons_col] = row[pounds_col] / self.conversion_factor
        
        # Memperbarui cleaned_data dengan data yang sudah diperbaiki
        self.cleaned_data = fixed_data
        
        print("Perbaikan data selesai.")
        
        # Memverifikasi kembali konsistensi
        print("Memverifikasi kembali konsistensi data...")
        expected_pounds = self.cleaned_data[metric_tons_col] * self.conversion_factor
        diff_pounds = abs(self.cleaned_data[pounds_col] - expected_pounds)
        tolerance_pounds = 0.01 * self.cleaned_data[pounds_col]
        still_inconsistent = diff_pounds > tolerance_pounds
        
        still_inconsistent_count = still_inconsistent.sum()
        print(f"Jumlah baris yang masih tidak konsisten setelah perbaikan: {still_inconsistent_count}")
        
        return True
    
    def generate_report(self):
        """
        Membuat laporan hasil analisis data
        """
        if self.original_data is None or self.cleaned_data is None:
            print("Analisis belum selesai. Jalankan semua metode analisis terlebih dahulu.")
            return False
            
        print(f"\n=== LAPORAN ANALISIS DATA TUNA ===")
        print(f"Tanggal pembuatan laporan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n1. Ringkasan Dataset:")
        print(f"   - Total baris awal: {len(self.original_data)}")
        print(f"   - Total baris setelah pembersihan: {len(self.cleaned_data)}")
        print(f"   - Persentase data yang tersimpan: {(len(self.cleaned_data)/len(self.original_data))*100:.2f}%")
        
        # Mencari kolom penting (case-insensitive)
        pounds_col = None
        metric_tons_col = None
        year_col = None
        state_col = None
        nmfs_name_col = None
        
        for col in self.cleaned_data.columns:
            col_lower = col.lower()
            if col_lower == 'pounds':
                pounds_col = col
            elif col_lower == 'metric tons':
                metric_tons_col = col
            elif col_lower == 'year':
                year_col = col
            elif col_lower == 'state':
                state_col = col
            elif col_lower == 'nmfs name':
                nmfs_name_col = col
        
        print(f"\n2. Statistik Data Setelah Pembersihan:")
        if pounds_col and metric_tons_col:
            print(f"   - Rata-rata {pounds_col}: {self.cleaned_data[pounds_col].mean():.2f}")
            print(f"   - Rata-rata {metric_tons_col}: {self.cleaned_data[metric_tons_col].mean():.2f}")
            print(f"   - Total {pounds_col}: {self.cleaned_data[pounds_col].sum():.2f}")
            print(f"   - Total {metric_tons_col}: {self.cleaned_data[metric_tons_col].sum():.2f}")
        
        if year_col:
            print(f"\n3. Rentang Tahun Data:")
            print(f"   - Tahun awal: {self.cleaned_data[year_col].min()}")
            print(f"   - Tahun akhir: {self.cleaned_data[year_col].max()}")
        
        if state_col:
            print(f"\n4. Jumlah Negara Bagian:")
            print(f"   - Total negara bagian: {self.cleaned_data[state_col].nunique()}")
            print(f"   - Negara bagian dengan data terbanyak: {self.cleaned_data[state_col].value_counts().index[0]} ({self.cleaned_data[state_col].value_counts().iloc[0]} records)")
        
        if nmfs_name_col:
            print(f"\n5. Jenis Ikan:")
            print(f"   - Total jenis ikan: {self.cleaned_data[nmfs_name_col].nunique()}")
            top_species = self.cleaned_data[nmfs_name_col].value_counts().head(3)
            print(f"   - 3 jenis ikan terbanyak:")
            for species, count in top_species.items():
                print(f"     * {species}: {count} records")
        
        return True
    
    def save_cleaned_data(self, output_filename="tuna_data_final_cleaned.xlsx"):
        """
        Menyimpan data yang sudah dibersihkan ke file Excel baru
        """
        if self.cleaned_data is None:
            print("Data belum dibersihkan. Jalankan clean_data() terlebih dahulu.")
            return False
            
        try:
            self.cleaned_data.to_excel(output_filename, index=False)
            print(f"\nData yang sudah dibersihkan berhasil disimpan ke: {output_filename}")
            return True
        except Exception as e:
            print(f"Error saat menyimpan data: {str(e)}")
            return False
    
    def create_visualization(self):
        """
        Membuat visualisasi data
        """
        if self.cleaned_data is None:
            print("Data belum dibersihkan. Jalankan clean_data() terlebih dahulu.")
            return False
            
        try:
            # Mencari kolom penting (case-insensitive)
            pounds_col = None
            metric_tons_col = None
            year_col = None
            
            for col in self.cleaned_data.columns:
                col_lower = col.lower()
                if col_lower == 'pounds':
                    pounds_col = col
                elif col_lower == 'metric tons':
                    metric_tons_col = col
                elif col_lower == 'year':
                    year_col = col
            
            if not pounds_col or not metric_tons_col:
                print("Kolom 'pounds' atau 'metric tons' tidak ditemukan untuk visualisasi.")
                return False
            
            # Visualisasi 1: Distribusi pounds vs metric tons
            plt.figure(figsize=(12, 6))
            
            plt.subplot(1, 2, 1)
            plt.scatter(self.cleaned_data[metric_tons_col], self.cleaned_data[pounds_col], alpha=0.5)
            plt.xlabel('Metric Tons')
            plt.ylabel('Pounds')
            plt.title('Hubungan antara Metric Tons dan Pounds')
            
            # Garis referensi konversi yang benar
            max_metric = self.cleaned_data[metric_tons_col].max()
            x_ref = np.linspace(0, max_metric, 100)
            y_ref = x_ref * self.conversion_factor
            plt.plot(x_ref, y_ref, 'r-', label=f'Konversi Ideal (1 ton = {self.conversion_factor} lbs)')
            plt.legend()
            
            # Visualisasi 2: Total tangkapan per tahun (jika kolom year ada)
            if year_col:
                plt.subplot(1, 2, 2)
                yearly_catch = self.cleaned_data.groupby(year_col)[metric_tons_col].sum()
                plt.plot(yearly_catch.index, yearly_catch.values)
                plt.xlabel('Tahun')
                plt.ylabel('Total Tangkapan (Metric Tons)')
                plt.title('Total Tangkapan per Tahun')
                plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig('tuna_data_visualization.png', dpi=300, bbox_inches='tight')
            print("Visualisasi berhasil disimpan ke: tuna_data_visualization.png")
            return True
            
        except Exception as e:
            print(f"Error saat membuat visualisasi: {str(e)}")
            return False
    
    def run_full_analysis(self):
        """
        Menjalankan seluruh proses analisis data
        """
        print("=== MEMULAI ANALISIS DATA TUNA ===")
        
        # 1. Memuat data
        if not self.load_data():
            return False
        
        # 2. Menganalisis struktur
        self.analyze_structure()
        
        # 3. Mengidentifikasi baris kosong
        empty_rows = self.identify_empty_rows()
        
        # 4. Membersihkan data
        if not self.clean_data():
            return False
        
        # 5. Memeriksa konsistensi
        inconsistent_rows = self.check_consistency()
        
        # 6. Memperbaiki data tidak konsisten
        if inconsistent_rows is not None and inconsistent_rows.sum() > 0:
            self.fix_inconsistent_data(inconsistent_rows)
        
        # 7. Membuat laporan
        self.generate_report()
        
        # 8. Menyimpan data yang sudah dibersihkan
        self.save_cleaned_data()
        
        # 9. Membuat visualisasi
        self.create_visualization()
        
        print("\n=== ANALISIS DATA SELESAI ===")
        return True

# Fungsi utama untuk menjalankan program
def main():
    # Path ke file Excel
    file_path = "tuna_data_fixed.xlsx"
    
    # Membuat instance analyzer
    analyzer = TunaDataAnalyzer(file_path)
    
    # Menjalankan analisis lengkap
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()