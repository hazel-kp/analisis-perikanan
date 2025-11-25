#!/usr/bin/env python3
"""
Skrip untuk menjalankan analisis data tuna dengan pemeriksaan dependensi
"""

import sys
import subprocess
import importlib

def check_and_install_dependencies():
    """
    Memeriksa dan menginstal dependensi yang diperlukan
    """
    print("Memeriksa dependensi yang diperlukan...")
    
    required_packages = [
        'pandas',
        'numpy', 
        'matplotlib',
        'openpyxl',
        'xlrd'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"[OK] {package} sudah terinstall")
        except ImportError:
            print(f"[MISSING] {package} belum terinstall")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMenginstal package yang hilang: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("Semua dependensi berhasil diinstall!")
        except subprocess.CalledProcessError as e:
            print(f"Error saat menginstall dependensi: {e}")
            return False
    
    return True

def main():
    """
    Fungsi utama untuk menjalankan analisis
    """
    print("=== ANALISIS DATA TUNA ===")
    print("Program ini akan menganalisis data tuna yang sudah diperbaiki dari file tuna_data_fixed.xlsx")
    print()
    
    # Memeriksa dan menginstall dependensi
    if not check_and_install_dependencies():
        print("Gagal menginstall dependensi. Silakan install manual dengan: pip install -r requirements.txt")
        return
    
    print("\nMemulai analisis data...")
    
    try:
        # Import dan jalankan analyzer
        from analyze_tuna_data import TunaDataAnalyzer
        
        # Path ke file Excel yang sudah diperbaiki
        file_path = "tuna_data_fixed.xlsx"
        
        # Membuat instance analyzer
        analyzer = TunaDataAnalyzer(file_path)
        
        # Menjalankan analisis lengkap
        success = analyzer.run_full_analysis()
        
        if success:
            print("\n[SUCCESS] Analisis data selesai dengan sukses!")
            print("\nFile yang dihasilkan:")
            print("1. tuna_data_final_cleaned.xlsx - Data final yang sudah dibersihkan dan dianalisis")
            print("2. tuna_data_visualization.png - Visualisasi data")
        else:
            print("\n[ERROR] Analisis data gagal. Silakan periksa error di atas.")
            
    except ImportError as e:
        print(f"Error saat mengimport modul: {e}")
        print("Pastikan semua dependensi sudah terinstall dengan benar.")
    except Exception as e:
        print(f"Error saat menjalankan analisis: {e}")

if __name__ == "__main__":
    main()