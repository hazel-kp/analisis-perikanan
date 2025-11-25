import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style untuk visualisasi yang lebih menarik
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_comprehensive_visualizations(input_file):
    """
    Membuat berbagai visualisasi komprehensif dari data tuna
    """
    
    # Memuat data
    print(f"Memuat data dari {input_file}...")
    df = pd.read_excel(input_file)
    print(f"Data berhasil dimuat: {len(df)} baris")
    
    # Mencari kolom penting (case-insensitive)
    nmfs_col = None
    source_col = None
    year_col = None
    metric_tons_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if col_lower == 'nmfs name':
            nmfs_col = col
        elif col_lower == 'source':
            source_col = col
        elif col_lower == 'year':
            year_col = col
        elif col_lower == 'metric tons':
            metric_tons_col = col
    
    if not all([nmfs_col, source_col, year_col, metric_tons_col]):
        print("Error: Kolom yang diperlukan tidak ditemukan")
        return False
    
    # 1. Bar Chart untuk NMFS Name Distribution
    print("Membuat bar chart untuk NMFS Name distribution...")
    plt.figure(figsize=(16, 10))
    nmfs_counts = df[nmfs_col].value_counts()
    bars = plt.bar(range(len(nmfs_counts)), nmfs_counts.values,
                   color='skyblue', edgecolor='navy', alpha=0.8, linewidth=1)
    plt.title('Distribusi Jenis Ikan Tuna (NMFS Name)', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Jenis Ikan', fontsize=14, fontweight='bold')
    plt.ylabel('Jumlah Records', fontsize=14, fontweight='bold')
    plt.xticks(range(len(nmfs_counts)), nmfs_counts.index, rotation=45, ha='right', fontsize=11)
    plt.yticks(fontsize=11)
    
    # Mengatur skala y-axis yang lebih baik
    max_count = nmfs_counts.max()
    plt.ylim(0, max_count * 1.15)
    
    # Menambahkan grid untuk kemudahan membaca
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Menambahkan nilai di atas bar dengan garis penghubung
    for i, bar in enumerate(bars):
        height = bar.get_height()
        x_pos = bar.get_x() + bar.get_width()/2.
        
        # Garis penghubung dari puncak bar ke nilai
        plt.plot([x_pos, x_pos], [height, height + max_count * 0.02],
                'k-', linewidth=1, alpha=0.6)
        
        # Titik di puncak bar
        plt.plot(x_pos, height, 'ko', markersize=4)
        
        # Teks nilai
        plt.text(x_pos, height + max_count * 0.03, f'{int(height):,}',
                ha='center', va='bottom', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('nmfs_name_distribution_improved.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Pie Chart untuk Source Distribution
    print("Membuat pie chart untuk Source distribution...")
    plt.figure(figsize=(10, 8))
    source_counts = df[source_col].value_counts()
    colors = plt.cm.Set3(np.linspace(0, 1, len(source_counts)))
    
    wedges, texts, autotexts = plt.pie(source_counts.values, labels=source_counts.index, 
                                      autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title('Distribusi Sumber Data (Source)', fontsize=16, fontweight='bold')
    
    # Mempercantik text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('source_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Stacked Pie Chart untuk Yellowfin vs Bluefin per tahun
    print("Membuat stacked pie chart untuk Yellowfin vs Bluefin per tahun...")
    yellowfin_data = df[df[nmfs_col].str.contains('YELLOWFIN', case=False, na=False)]
    bluefin_data = df[df[nmfs_col].str.contains('BLUEFIN', case=False, na=False)]
    
    # Mengelompokkan per tahun
    yellowfin_yearly = yellowfin_data.groupby(year_col)[metric_tons_col].sum()
    bluefin_yearly = bluefin_data.groupby(year_col)[metric_tons_col].sum()
    
    # Menggabungkan data
    combined_years = sorted(set(yellowfin_yearly.index) | set(bluefin_yearly.index))
    yellowfin_values = [yellowfin_yearly.get(year, 0) for year in combined_years]
    bluefin_values = [bluefin_yearly.get(year, 0) for year in combined_years]
    
    # Membuat stacked bar chart dengan peningkatan keterbacaan
    plt.figure(figsize=(16, 10))
    width = 0.7
    x_pos = np.arange(len(combined_years))
    
    bars1 = plt.bar(x_pos, yellowfin_values, width, label='Yellowfin Tuna',
                    color='gold', edgecolor='darkorange', alpha=0.8, linewidth=1)
    bars2 = plt.bar(x_pos, bluefin_values, width, bottom=yellowfin_values,
                    label='Bluefin Tuna', color='royalblue', edgecolor='navy',
                    alpha=0.8, linewidth=1)
    
    plt.title('Perbandingan Tangkapan Yellowfin vs Bluefin Tuna per Tahun',
             fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Tahun', fontsize=14, fontweight='bold')
    plt.ylabel('Total Tangkapan (Metric Tons)', fontsize=14, fontweight='bold')
    plt.xticks(x_pos, combined_years, rotation=45, fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend(fontsize=12, loc='upper left')
    
    # Mengatur skala y-axis yang lebih baik
    max_total = max([y + b for y, b in zip(yellowfin_values, bluefin_values)])
    plt.ylim(0, max_total * 1.15)
    
    # Menambahkan grid untuk kemudahan membaca
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Menambahkan nilai dan garis penghubung untuk setiap bar
    for i, (y_val, b_val) in enumerate(zip(yellowfin_values, bluefin_values)):
        x_pos_bar = x_pos[i]
        
        # Untuk Yellowfin (bagian bawah)
        if y_val > 0:
            # Garis penghubung dan nilai untuk Yellowfin
            plt.plot([x_pos_bar, x_pos_bar], [y_val, y_val + max_total * 0.01],
                    'k-', linewidth=1, alpha=0.6)
            plt.plot(x_pos_bar, y_val, 'ko', markersize=3)
            plt.text(x_pos_bar, y_val + max_total * 0.015, f'{y_val:,.0f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.7))
        
        # Untuk Bluefin (bagian atas)
        total_val = y_val + b_val
        if b_val > 0:
            # Garis penghubung dan nilai untuk Bluefin
            plt.plot([x_pos_bar, x_pos_bar], [total_val, total_val + max_total * 0.01],
                    'k-', linewidth=1, alpha=0.6)
            plt.plot(x_pos_bar, total_val, 'ko', markersize=3)
            plt.text(x_pos_bar, total_val + max_total * 0.015, f'{total_val:,.0f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('yellowfin_vs_bluefin_yearly_improved.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Stacked Column Chart untuk jenis ikan dari tahun 2010-2020
    print("Membuat stacked column chart untuk jenis ikan (2010-2020)...")
    filtered_data = df[(df[year_col] >= 2010) & (df[year_col] <= 2020)]
    
    # Membuat pivot table
    pivot_data = filtered_data.pivot_table(
        values=metric_tons_col, 
        index=year_col, 
        columns=nmfs_col, 
        aggfunc='sum', 
        fill_value=0
    )
    
    plt.figure(figsize=(18, 12))
    ax = pivot_data.plot(kind='bar', stacked=True, figsize=(18, 12),
                         edgecolor='black', linewidth=0.5, alpha=0.8)
    
    plt.title('Distribusi Jenis Ikan Tuna per Tahun (2010-2020)',
             fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Tahun', fontsize=14, fontweight='bold')
    plt.ylabel('Total Tangkapan (Metric Tons)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Jenis Ikan', bbox_to_anchor=(1.05, 1), loc='upper left',
              fontsize=11, title_fontsize=12)
    
    # Mengatur skala y-axis yang lebih baik
    max_total = pivot_data.sum(axis=1).max()
    plt.ylim(0, max_total * 1.15)
    
    # Menambahkan grid untuk kemudahan membaca
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Menambahkan nilai total di atas setiap stacked bar dengan garis penghubung
    for i, year in enumerate(pivot_data.index):
        total = pivot_data.loc[year].sum()
        if total > 0:
            x_pos = i
            
            # Garis penghubung dari puncak bar ke nilai
            plt.plot([x_pos, x_pos], [total, total + max_total * 0.01],
                    'k-', linewidth=1, alpha=0.6)
            
            # Titik di puncak bar
            plt.plot(x_pos, total, 'ko', markersize=4)
            
            # Teks nilai total
            plt.text(x_pos, total + max_total * 0.02, f'{total:,.0f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('fish_types_2010_2020_improved.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Line Chart untuk jenis ikan per tahun
    print("Membuat line chart untuk jenis ikan per tahun...")
    plt.figure(figsize=(18, 12))
    
    # Mengelompokkan data per tahun dan jenis ikan
    yearly_species_data = df.groupby([year_col, nmfs_col])[metric_tons_col].sum().reset_index()
    
    # Mengatur warna yang berbeda untuk setiap jenis ikan
    colors = plt.cm.tab10(np.linspace(0, 1, len(df[nmfs_col].unique())))
    
    # Membuat line chart untuk setiap jenis ikan dengan peningkatan keterbacaan
    for i, species in enumerate(df[nmfs_col].unique()):
        species_data = yearly_species_data[yearly_species_data[nmfs_col] == species]
        
        # Plot line dengan marker yang lebih jelas
        plt.plot(species_data[year_col], species_data[metric_tons_col],
                marker='o', linewidth=2.5, markersize=6, label=species,
                color=colors[i], markeredgecolor='black', markeredgewidth=0.5)
        
        # Menambahkan nilai di setiap titik dengan garis penghubung
        for _, row in species_data.iterrows():
            year_val = row[year_col]
            metric_val = row[metric_tons_col]
            
            if metric_val > 0:
                # Garis penghubung vertikal dari line ke nilai
                plt.plot([year_val, year_val], [metric_val, metric_val + (df[metric_tons_col].max() * 0.02)],
                        'k-', linewidth=0.8, alpha=0.5)
                
                # Teks nilai dengan background
                plt.text(year_val, metric_val + (df[metric_tons_col].max() * 0.025),
                        f'{metric_val:,.0f}',
                        ha='center', va='bottom', fontsize=8, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    plt.title('Trend Tangkapan Jenis Ikan Tuna per Tahun',
             fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Tahun', fontsize=14, fontweight='bold')
    plt.ylabel('Total Tangkapan (Metric Tons)', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    
    # Mengatur skala y-axis yang lebih baik
    max_metric = df[metric_tons_col].max()
    plt.ylim(0, max_metric * 1.15)
    
    # Menambahkan grid yang lebih jelas
    plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Mempercantik legend
    plt.legend(title='Jenis Ikan', bbox_to_anchor=(1.05, 1), loc='upper left',
              fontsize=11, title_fontsize=12, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig('fish_types_trend_improved.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Dashboard dengan semua visualisasi
    print("Membuat dashboard komprehensif...")
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Dashboard Analisis Data Tuna Komprehensif', fontsize=20, fontweight='bold')
    
    # Bar chart NMFS Name
    axes[0, 0].bar(range(len(nmfs_counts)), nmfs_counts.values)
    axes[0, 0].set_title('Distribusi Jenis Ikan')
    axes[0, 0].set_xticks(range(len(nmfs_counts)))
    axes[0, 0].set_xticklabels(nmfs_counts.index, rotation=45, ha='right')
    
    # Pie chart Source
    axes[0, 1].pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%')
    axes[0, 1].set_title('Distribusi Sumber Data')
    
    # Yellowfin vs Bluefin
    x_pos = np.arange(len(combined_years[-10:]))  # 10 tahun terakhir
    axes[0, 2].bar(x_pos, yellowfin_values[-10:], width, label='Yellowfin')
    axes[0, 2].bar(x_pos, bluefin_values[-10:], width, bottom=yellowfin_values[-10:], label='Bluefin')
    axes[0, 2].set_title('Yellowfin vs Bluefin (10 Tahun Terakhir)')
    axes[0, 2].set_xticks(x_pos)
    axes[0, 2].set_xticklabels(combined_years[-10:], rotation=45)
    axes[0, 2].legend()
    
    # Stacked column 2010-2020
    pivot_data.plot(kind='bar', stacked=True, ax=axes[1, 0], legend=False)
    axes[1, 0].set_title('Jenis Ikan (2010-2020)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Line chart trend
    for species in df[nmfs_col].unique()[:5]:  # 5 jenis teratas
        species_data = yearly_species_data[yearly_species_data[nmfs_col] == species]
        axes[1, 1].plot(species_data[year_col], species_data[metric_tons_col], 
                       marker='o', label=species)
    axes[1, 1].set_title('Trend 5 Jenis Ikan Teratas')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    # Statistik summary
    axes[1, 2].axis('off')
    stats_text = f"""
    Statistik Data:
    Total Records: {len(df):,}
    Rentang Tahun: {df[year_col].min()} - {df[year_col].max()}
    Total Jenis Ikan: {df[nmfs_col].nunique()}
    Total Sumber: {df[source_col].nunique()}
    
    Top 3 Jenis Ikan:
    1. {df[nmfs_col].value_counts().index[0]}
    2. {df[nmfs_col].value_counts().index[1]}
    3. {df[nmfs_col].value_counts().index[2]}
    
    Total Tangkapan:
    {df[metric_tons_col].sum():,.0f} Metric Tons
    """
    axes[1, 2].text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig('tuna_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n=== VISUALISASI SELESAI ===")
    print("File yang dihasilkan:")
    print("1. nmfs_name_distribution.png - Bar chart distribusi jenis ikan")
    print("2. source_distribution.png - Pie chart distribusi sumber data")
    print("3. yellowfin_vs_bluefin_yearly.png - Perbandingan Yellowfin vs Bluefin")
    print("4. fish_types_2010_2020.png - Stacked column chart 2010-2020")
    print("5. fish_types_trend.png - Line chart trend per tahun")
    print("6. tuna_dashboard.png - Dashboard komprehensif")
    
    return True

if __name__ == "__main__":
    input_file = "tuna_data_final_cleaned.xlsx"
    success = create_comprehensive_visualizations(input_file)
    
    if success:
        print("\nSemua visualisasi berhasil dibuat!")
    else:
        print("\nGagal membuat visualisasi.")