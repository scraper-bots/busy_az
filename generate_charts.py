"""
Business Intelligence Dashboard - Busy.az Candidate Analysis
Generates comprehensive business-focused visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import re
import warnings
warnings.filterwarnings('ignore')

# Set professional styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# Load data
df = pd.read_csv('busy_az_candidates.csv')

# Data cleaning and preparation
def extract_numeric_salary(salary_str):
    """Extract numeric salary values from text"""
    if pd.isna(salary_str):
        return np.nan
    if 'Razılaşma' in str(salary_str) or str(salary_str).strip() == 'AZN':
        return np.nan

    # Extract numbers from salary string
    numbers = re.findall(r'\d+(?:\.\d+)?', str(salary_str))
    if numbers:
        # If range (e.g., "500-1000"), take the average
        nums = [float(n) for n in numbers]
        return np.mean(nums)
    return np.nan

df['salary_numeric'] = df['salary_expectation'].apply(extract_numeric_salary)

# Clean gender data
df['gender_clean'] = df['gender'].fillna('Məlum deyil')

# Extract language skills
def extract_languages(lang_str):
    """Extract languages from language string"""
    if pd.isna(lang_str):
        return []
    languages = []
    if 'İngilis' in str(lang_str) or 'English' in str(lang_str):
        languages.append('İngilis')
    if 'Rus' in str(lang_str) or 'Russian' in str(lang_str):
        languages.append('Rus')
    if 'Azərbaycan' in str(lang_str):
        languages.append('Azərbaycan')
    if 'Türk' in str(lang_str):
        languages.append('Türk')
    return languages

df['languages_list'] = df['languages'].apply(extract_languages)

# Chart 1: Gender Distribution
def chart_gender_distribution():
    """Gender distribution in candidate pool"""
    fig, ax = plt.subplots(figsize=(10, 6))

    gender_counts = df['gender_clean'].value_counts()
    colors = ['#2E86AB', '#A23B72', '#F18F01']

    bars = ax.barh(range(len(gender_counts)), gender_counts.values, color=colors[:len(gender_counts)])
    ax.set_yticks(range(len(gender_counts)))
    ax.set_yticklabels(gender_counts.index)
    ax.set_xlabel('Namizədlərin sayı')
    ax.set_title('Namizəd bazasında gender tərkibi', fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, gender_counts.values)):
        percentage = (value / len(df)) * 100
        ax.text(value + 10, i, f'{value} ({percentage:.1f}%)',
                va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/01_gender_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Gender Distribution")

# Chart 2: Top 15 In-Demand Positions
def chart_top_positions():
    """Most sought-after positions by candidates"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Filter out age entries that mistakenly appear as positions
    positions = df['position'].dropna()
    positions = positions[~positions.str.contains('yaş', na=False)]

    top_positions = positions.value_counts().head(15)

    bars = ax.barh(range(len(top_positions)), top_positions.values, color='#2E86AB')
    ax.set_yticks(range(len(top_positions)))
    ax.set_yticklabels(top_positions.index)
    ax.set_xlabel('Namizəd sayı')
    ax.set_title('Ən çox axtarılan TOP 15 vəzifə', fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_positions.values)):
        ax.text(value + 0.5, i, str(value), va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/02_top_positions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Top Positions")

# Chart 3: Salary Expectations Distribution
def chart_salary_distribution():
    """Salary expectations among candidates"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Left: Negotiable vs Specific
    salary_category = df['salary_expectation'].apply(
        lambda x: 'Razılaşma əsasında' if pd.isna(x) or 'Razılaşma' in str(x) or str(x).strip() == 'AZN' else 'Konkret məbləğ'
    )
    cat_counts = salary_category.value_counts()

    colors = ['#F18F01', '#2E86AB']
    bars = ax1.bar(range(len(cat_counts)), cat_counts.values, color=colors)
    ax1.set_xticks(range(len(cat_counts)))
    ax1.set_xticklabels(cat_counts.index, rotation=0)
    ax1.set_ylabel('Namizəd sayı')
    ax1.set_title('Maaş gözləntisi: Razılaşma vs Konkret məbləğ', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    for bar, value in zip(bars, cat_counts.values):
        percentage = (value / len(df)) * 100
        ax1.text(bar.get_x() + bar.get_width()/2, value + 10,
                f'{value}\n({percentage:.1f}%)', ha='center', fontweight='bold')

    # Right: Salary ranges for those who specified
    salary_numeric = df['salary_numeric'].dropna()
    salary_ranges = pd.cut(salary_numeric, bins=[0, 500, 1000, 1500, 2000, 10000],
                           labels=['0-500 AZN', '500-1000 AZN', '1000-1500 AZN',
                                  '1500-2000 AZN', '2000+ AZN'])
    range_counts = salary_ranges.value_counts().sort_index()

    bars = ax2.bar(range(len(range_counts)), range_counts.values, color='#A23B72')
    ax2.set_xticks(range(len(range_counts)))
    ax2.set_xticklabels(range_counts.index, rotation=45, ha='right')
    ax2.set_ylabel('Namizəd sayı')
    ax2.set_title('Maaş intervalları (konkret məbləğ göstərənlər)', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)

    for bar, value in zip(bars, range_counts.values):
        ax2.text(bar.get_x() + bar.get_width()/2, value + 1,
                str(value), ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/03_salary_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Salary Distribution")

# Chart 4: Average Salary by Top Positions
def chart_salary_by_position():
    """Average salary expectations by position"""
    # Filter valid positions and salaries
    df_valid = df[df['salary_numeric'].notna()].copy()
    df_valid = df_valid[~df_valid['position'].str.contains('yaş', na=False)]

    # Get positions with at least 5 candidates
    position_counts = df_valid['position'].value_counts()
    valid_positions = position_counts[position_counts >= 3].index

    df_filtered = df_valid[df_valid['position'].isin(valid_positions)]

    # Calculate average salary by position
    avg_salary = df_filtered.groupby('position')['salary_numeric'].mean().sort_values(ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(12, 8))

    bars = ax.barh(range(len(avg_salary)), avg_salary.values, color='#06A77D')
    ax.set_yticks(range(len(avg_salary)))
    ax.set_yticklabels(avg_salary.index)
    ax.set_xlabel('Orta maaş gözləntisi (AZN)')
    ax.set_title('Vəzifələr üzrə orta maaş gözləntisi (TOP 15)', fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, avg_salary.values)):
        ax.text(value + 20, i, f'{value:.0f} AZN', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/04_salary_by_position.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Salary by Position")

# Chart 5: Language Skills Distribution
def chart_language_skills():
    """Language capabilities in candidate pool"""
    # Count language occurrences
    all_languages = []
    for langs in df['languages_list']:
        all_languages.extend(langs)

    from collections import Counter
    lang_counts = Counter(all_languages)
    lang_df = pd.DataFrame.from_dict(lang_counts, orient='index', columns=['count']).sort_values('count', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(range(len(lang_df)), lang_df['count'].values, color='#E63946')
    ax.set_xticks(range(len(lang_df)))
    ax.set_xticklabels(lang_df.index, rotation=0)
    ax.set_ylabel('Namizəd sayı')
    ax.set_title('Namizədlərin dil bilikləri', fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar, value in zip(bars, lang_df['count'].values):
        percentage = (value / len(df)) * 100
        ax.text(bar.get_x() + bar.get_width()/2, value + 5,
                f'{value}\n({percentage:.1f}%)', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/05_language_skills.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Language Skills")

# Chart 6: Data Completeness Profile
def chart_data_completeness():
    """Profile completeness analysis"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Calculate completeness for key fields
    fields = ['skills', 'languages', 'education', 'work_history', 'about']
    field_labels = ['Bacarıqlar', 'Dillər', 'Təhsil', 'İş təcrübəsi', 'Haqqında']

    completeness = []
    for field in fields:
        complete = df[field].notna().sum()
        percentage = (complete / len(df)) * 100
        completeness.append(percentage)

    colors = ['#06A77D' if p >= 50 else '#F18F01' if p >= 30 else '#E63946' for p in completeness]

    bars = ax.barh(range(len(field_labels)), completeness, color=colors)
    ax.set_yticks(range(len(field_labels)))
    ax.set_yticklabels(field_labels)
    ax.set_xlabel('Doldurulma faizi (%)')
    ax.set_title('Namizəd profilinin dolulluq dərəcəsi', fontweight='bold', pad=20)
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    # Add percentage labels
    for i, (bar, value) in enumerate(zip(bars, completeness)):
        ax.text(value + 2, i, f'{value:.1f}%', va='center', fontweight='bold')

    # Add reference line at 50%
    ax.axvline(x=50, color='gray', linestyle='--', alpha=0.5, label='50% meyar')
    ax.legend()

    plt.tight_layout()
    plt.savefig('charts/06_profile_completeness.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Profile Completeness")

# Chart 7: Contact Information Availability
def chart_contact_availability():
    """Contact information completeness"""
    fig, ax = plt.subplots(figsize=(10, 6))

    contact_fields = {
        'Mobil telefon': df['mobile_phone'].notna().sum(),
        'Ev telefonu': df['home_phone'].notna().sum(),
        'Email': df['email'].notna().sum()
    }

    categories = list(contact_fields.keys())
    values = list(contact_fields.values())
    percentages = [(v / len(df)) * 100 for v in values]

    bars = ax.bar(range(len(categories)), percentages, color=['#2E86AB', '#A23B72', '#06A77D'])
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)
    ax.set_ylabel('Doldurulma faizi (%)')
    ax.set_title('Əlaqə məlumatlarının mövcudluğu', fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    # Add labels
    for bar, value, count in zip(bars, percentages, values):
        ax.text(bar.get_x() + bar.get_width()/2, value + 2,
                f'{value:.1f}%\n({count})', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/07_contact_availability.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Contact Availability")

# Chart 8: Position Categories
def chart_position_categories():
    """Candidate distribution by job category"""
    # Categorize positions
    def categorize_position(pos):
        if pd.isna(pos):
            return 'Digər'
        pos_lower = str(pos).lower()

        if 'satış' in pos_lower or 'sales' in pos_lower:
            return 'Satış'
        elif 'mühasib' in pos_lower or 'account' in pos_lower:
            return 'Maliyyə və Mühasibat'
        elif 'mühəndis' in pos_lower or 'engineer' in pos_lower:
            return 'Mühəndislik'
        elif 'marketing' in pos_lower or 'smm' in pos_lower or 'brand' in pos_lower:
            return 'Marketinq'
        elif 'developer' in pos_lower or 'proqramçı' in pos_lower or 'programmer' in pos_lower:
            return 'İT və Proqramlaşdırma'
        elif 'dizayn' in pos_lower or 'design' in pos_lower:
            return 'Dizayn'
        elif 'hüquq' in pos_lower or 'lawyer' in pos_lower:
            return 'Hüquq'
        elif 'sürücü' in pos_lower or 'driver' in pos_lower:
            return 'Nəqliyyat'
        elif 'konstruktor' in pos_lower:
            return 'İnşaat'
        elif 'hr' in pos_lower or 'insan resurs' in pos_lower:
            return 'İnsan Resursları'
        else:
            return 'Digər'

    df['category'] = df['position'].apply(categorize_position)
    category_counts = df['category'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(range(len(category_counts)), category_counts.values,
                   color=plt.cm.Set3(range(len(category_counts))))
    ax.set_yticks(range(len(category_counts)))
    ax.set_yticklabels(category_counts.index)
    ax.set_xlabel('Namizəd sayı')
    ax.set_title('Namizədlərin sahələr üzrə paylanması', fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, category_counts.values)):
        percentage = (value / len(df)) * 100
        ax.text(value + 2, i, f'{value} ({percentage:.1f}%)', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/08_position_categories.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Position Categories")

# Chart 9: Salary Negotiability by Gender
def chart_salary_by_gender():
    """Salary negotiation preferences by gender"""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create salary category
    df['salary_type'] = df['salary_expectation'].apply(
        lambda x: 'Razılaşma əsasında' if pd.isna(x) or 'Razılaşma' in str(x) or str(x).strip() == 'AZN' else 'Konkret məbləğ'
    )

    # Create cross-tabulation
    cross_tab = pd.crosstab(df['gender_clean'], df['salary_type'])
    cross_tab_pct = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100

    # Filter to main genders only
    if 'Kişi' in cross_tab_pct.index and 'Qadın' in cross_tab_pct.index:
        cross_tab_pct = cross_tab_pct.loc[['Kişi', 'Qadın']]

    cross_tab_pct.plot(kind='bar', ax=ax, color=['#F18F01', '#2E86AB'], width=0.7)
    ax.set_xlabel('Gender')
    ax.set_ylabel('Faiz (%)')
    ax.set_title('Maaş göstərmə meyli: Gender üzrə müqayisə', fontweight='bold', pad=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title='Maaş növü', loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    # Add percentage labels
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3)

    plt.tight_layout()
    plt.savefig('charts/09_salary_by_gender.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Salary by Gender")

# Chart 10: Multi-language Capability
def chart_multilingual_candidates():
    """Multilingual capabilities analysis"""
    df['num_languages'] = df['languages_list'].apply(len)

    lang_counts = df['num_languages'].value_counts().sort_index()
    lang_counts = lang_counts[lang_counts.index > 0]  # Exclude 0

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(range(len(lang_counts)), lang_counts.values, color='#A23B72')
    ax.set_xticks(range(len(lang_counts)))
    ax.set_xticklabels([f'{int(idx)} dil' for idx in lang_counts.index])
    ax.set_ylabel('Namizəd sayı')
    ax.set_title('Namizədlərin çoxdillilik göstəriciləri', fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar, value in zip(bars, lang_counts.values):
        percentage = (value / df[df['num_languages'] > 0].shape[0]) * 100
        ax.text(bar.get_x() + bar.get_width()/2, value + 5,
                f'{value}\n({percentage:.1f}%)', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('charts/10_multilingual_candidates.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Multilingual Candidates")

# Main execution
def main():
    print("\n" + "="*60)
    print("BUSY.AZ CANDIDATE DATABASE - BUSINESS INTELLIGENCE DASHBOARD")
    print("="*60 + "\n")
    print("Generating business-focused visualizations...\n")

    chart_gender_distribution()
    chart_top_positions()
    chart_salary_distribution()
    chart_salary_by_position()
    chart_language_skills()
    chart_data_completeness()
    chart_contact_availability()
    chart_position_categories()
    chart_salary_by_gender()
    chart_multilingual_candidates()

    print("\n" + "="*60)
    print("✓ All charts generated successfully in charts/ directory")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
