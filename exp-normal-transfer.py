import shutil
import csv
import os
from tqdm import tqdm

def copy_from_csv(csv_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    total_files = len(rows)
    with tqdm(total=total_files, desc="Copying files", unit="file", ncols=80) as pbar:
        for row in rows:
            src_file = row['FilePath']
            dest_file = os.path.join(dest_dir, os.path.basename(src_file))

            if not os.path.exists(dest_file):
                shutil.copy2(src_file, dest_file)

            pbar.update(1)
    
    print(f"\nAll files copied successfully to {dest_dir}.")
