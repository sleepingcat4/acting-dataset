import os
import shutil
import time
from tqdm import tqdm

def copy_mp3(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    total_files = sum(len(files) for _, _, files in os.walk(src_dir) if any(file.endswith('.mp3') for file in files))
    moved_files = 0
    start_time = time.time()

    with tqdm(total=total_files, desc="Copying files", unit="file", ncols=80) as pbar:
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.mp3'):
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_dir, file)
                    shutil.copy2(src_file_path, dest_file_path)
                    moved_files += 1

                    elapsed_time = time.time() - start_time
                    estimated_time = (elapsed_time / moved_files) * (total_files - moved_files)
                    hours = estimated_time // 3600
                    print(
                        f"Total files {total_files} | FILES MOVED: {moved_files}/{total_files} | EST. TIME: {hours:.1f} hours",
                        end="\r"
                    )
                    pbar.update(1)

    print("\nAll files copied successfully.")
