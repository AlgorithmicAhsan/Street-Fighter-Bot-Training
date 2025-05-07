import pandas as pd
import glob
import os

# Folder containing your CSV files
folder_path = os.getcwd()

# Get all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Merge all CSV files
merged_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Save to a new file
output_file = os.path.join(folder_path, "merged_output.csv")
merged_df.to_csv(output_file, index=False)

print(f"[✓] Merged {len(csv_files)} files into {output_file}")
