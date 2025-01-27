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
    moved_files = 0
    start_time = time.time()

    with tqdm(total=total_files, desc="Copying files", unit="file", ncols=80) as pbar:
        for row in rows:
            src_file = row['FilePath']
            dest_file = os.path.join(dest_dir, os.path.basename(src_file))

            if not os.path.exists(dest_file):
                shutil.copy2(src_file, dest_file)
                moved_files += 1

            elapsed_time = time.time() - start_time
            estimated_time = (elapsed_time / moved_files) * (total_files - moved_files)
            hours = estimated_time // 3600
            print(
                f"Total files {total_files} | FILES MOVED: {moved_files}/{total_files} | EST. TIME: {hours:.1f} hours",
                end="\r"
            )

            pbar.update(1)
    
    print("\nAll files copied successfully to {dest_dir}.")
