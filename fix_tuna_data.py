import pandas as pd
import numpy as np

def fix_scientific_names_and_remove_empty_dollars(input_file, output_file):
    """
    Memperbaiki scientific names berdasarkan NMFS names dan menghapus baris dengan nilai Dollars kosong
    """
    
    # Memuat data
    print(f"Memuat data dari {input_file}...")
    df = pd.read_excel(input_file)
    print(f"Data awal: {len(df)} baris")
    
    # Mapping NMFS Name ke Scientific Name yang benar
    nmfs_to_scientific = {
        'TUNA, ALBACORE': 'Thunnus alalunga',
        'TUNA, BIGEYE': 'Thunnus obesus',
        'TUNA, BLACK SKIPJACK': 'Euthynnus lineatus',
        'TUNA, BLACKFIN': 'Thunnus atlanticus',
        'TUNA, BLUEFIN': 'Thunnus thynnus',
        'TUNA, BLUEFIN PACIFIC': 'Thunnus orientalis',
        'TUNA, KAWAKAWA': 'Euthynnus affinis',
        'TUNA, LITTLE TUNNY': 'Euthynnus alletteratus',
        'TUNA, SKIPJACK': 'Katsuwonus pelamis',
        'TUNA, YELLOWFIN': 'Thunnus albacares'
    }
    
    # Memperbaiki Scientific Names
    print("Memperbaiki Scientific Names...")
    df['Scientific Name'] = df['NMFS Name'].map(nmfs_to_scientific)
    
    # Menampilkan jumlah scientific name yang diperbaiki
    fixed_count = len(df[df['Scientific Name'].notna()])
    print(f"Scientific Names yang diperbaiki: {fixed_count}")
    
    # Menghapus baris dengan nilai Dollars kosong
    print("Menghapus baris dengan nilai Dollars kosong...")
    initial_count = len(df)
    
    # Menghapus baris di mana Dollars adalah NaN, None, atau string kosong
    df_cleaned = df.dropna(subset=['Dollars'])
    
    # Juga menghapus baris di mana Dollars adalah string kosong atau whitespace
    df_cleaned = df_cleaned[df_cleaned['Dollars'].astype(str).str.strip() != '']
    
    final_count = len(df_cleaned)
    removed_count = initial_count - final_count
    
    print(f"Baris yang dihapus karena Dollars kosong: {removed_count}")
    print(f"Data akhir: {final_count} baris")
    
    # Menyimpan data yang sudah diperbaiki
    print(f"Menyimpan data yang sudah diperbaiki ke {output_file}...")
    df_cleaned.to_excel(output_file, index=False)
    
    # Menampilkan statistik akhir
    print("\n=== STATISTIK DATA SETELAH PERBAIKAN ===")
    print(f"Total baris: {len(df_cleaned)}")
    print(f"Jumlah NMFS Name unik: {df_cleaned['NMFS Name'].nunique()}")
    print(f"Jumlah Scientific Name unik: {df_cleaned['Scientific Name'].nunique()}")
    print(f"Jumlah State unik: {df_cleaned['State'].nunique()}")
    print(f"Rentang tahun: {df_cleaned['Year'].min()} - {df_cleaned['Year'].max()}")
    
    # Menampilkan mapping final
    print("\n=== MAPPING NMFS NAME KE SCIENTIFIC NAME ===")
    final_mapping = df_cleaned[['NMFS Name', 'Scientific Name']].drop_duplicates().sort_values('NMFS Name')
    print(final_mapping.to_string(index=False))
    
    return df_cleaned

if __name__ == "__main__":
    input_file = "tuna-fix.xlsx"
    output_file = "tuna_data_fixed.xlsx"
    
    df_cleaned = fix_scientific_names_and_remove_empty_dollars(input_file, output_file)
    
    print(f"\nData berhasil diperbaiki dan disimpan ke {output_file}")