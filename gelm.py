import pandas as pd
import numpy as np

# ==========================================
# 1. PRE-DEFINED REFERENCE MW BINS
# ==========================================
ALL_REFERENCE_MWS = [
    250, 300, 400, 450, 500, 600, 650, 700, 750, 
    900, 1000, 1250, 1400, 1500, 1750, 2000, 2200, 
    2500, 3000, 4000, 5000, 6000, 8000
]

# ==========================================
# 2. USER INPUTS (File Name & Max MW Limit)
# ==========================================
file_input = input("Enter the Excel file name (e.g. test.xlsx) [Press Enter for 'test.xlsx']: ").strip()

if not file_input:
    excel_file = 'test.xlsx'
else:
    excel_file = file_input if file_input.lower().endswith('.xlsx') else file_input + '.xlsx'

# Prompt user to dynamically set the maximum MW limit (e.g. 2200, 2500, 5000)
max_mw_input = input("Enter the maximum MW limit (e.g. 2200) [Press Enter for default 2200]: ").strip()

if not max_mw_input:
    max_mw_limit = 2200
else:
    try:
        max_mw_limit = float(max_mw_input)
    except ValueError:
        print("\n[WARNING]: Invalid input for Max MW. Defaulting to 2200.")
        max_mw_limit = 2200

# Filter reference bins strictly based on the user's dynamic limit
REFERENCE_MWS = [mw for mw in ALL_REFERENCE_MWS if mw <= max_mw_limit]
print(f"\nActive MW bins for analysis (up to {max_mw_limit}): {REFERENCE_MWS}")

try:
    # Read the raw Excel file handling raw Gel Analyzer exports correctly
    df_raw = pd.read_excel(excel_file, header=None)
    print(f"Reading file: '{excel_file}'...")
except FileNotFoundError:
    print(f"\n[ERROR]: File '{excel_file}' not found. Make sure it is in the same folder and closed in Excel!")
    exit()

if df_raw.empty:
    print(f"\n[ERROR]: The file '{excel_file}' is empty!")
    exit()

# ==========================================
# 3. PARSING GEL ANALYZER FORMAT
# ==========================================
# Handle single-column comma-separated exports from Gel Analyzer
if df_raw.shape[1] == 1:
    split_data = df_raw.iloc[:, 0].astype(str).str.split(',', expand=True)
    df = split_data.apply(lambda x: x.str.strip('"').str.strip("'"))
else:
    df = df_raw

# Drop header row if present
if 'Lane #' in str(df.iloc[0, 0]) or 'Lane' in str(df.iloc[0, 0]):
    df = df.iloc[1:].reset_index(drop=True)

# Column 0 = Lane #, Column 5 = MW (Molecular Weight)
lane_series = df.iloc[:, 0]
mw_series = df.iloc[:, 5]

# ==========================================
# 4. DATA CLEANING & FORMATTING
# ==========================================
def parse_lane(val):
    try:
        return int(float(str(val).strip()))
    except:
        return np.nan

lane_clean = lane_series.apply(parse_lane)

def parse_mw(val):
    try:
        s = str(val).strip().strip('"')
        if s == '-' or s == '':
            return np.nan
        if s.count('.') > 1:
            parts = s.split('.')
            s = ''.join(parts[:-1]) + '.' + parts[-1]
        return float(s)
    except:
        return np.nan

mw_clean = mw_series.apply(parse_mw)

# Build temporary working dataframe and drop invalid rows
clean_df = pd.DataFrame({'Lane': lane_clean, 'MW': mw_clean})
clean_df = clean_df.dropna(subset=['Lane', 'MW'])

# Exclude Lane 1 (Ladder) as requested
valid_mask = (clean_df['Lane'] != 1)
filtered_df = clean_df[valid_mask]

# ==========================================
# 5. BINARY MATRIX GENERATION WITH TOLERANCE (±5%)
# ==========================================
lanes = sorted(filtered_df['Lane'].unique())
result_data = []

for lane in lanes:
    lane_mw_values = filtered_df[filtered_df['Lane'] == lane]['MW'].values
    
    row = {'Lane #': lane}
    for ref_mw in REFERENCE_MWS:
        # 5% tolerance window to accommodate calibration drift
        tolerance = ref_mw * 0.05
        exists = any(abs(mw - ref_mw) <= tolerance for mw in lane_mw_values if not np.isnan(mw))
        row[str(ref_mw)] = 1 if exists else 0
        
    result_data.append(row)

result_df = pd.DataFrame(result_data)

# ==========================================
# 6. EXPORT RESULTS TO OUTPUT EXCEL
# ==========================================
output_file = excel_file.replace('.xlsx', f'_OUTPUT_{int(max_mw_limit)}.xlsx')
result_df.to_excel(output_file, index=False)

print(f"\nAnalysis completed successfully!")
print(f"Output file saved as: '{output_file}'")