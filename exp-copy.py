import os
import shutil

def exist_copy(input_folder, output_folder):
    mp3_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))

    total_subfolders = (len(mp3_files) + 999) // 1000
    print(f"Total subfolders to create in destination: {total_subfolders}")

    node_count = 1
    file_count = 0
    node_folder = os.path.join(output_folder, f"node{node_count}")
    os.makedirs(node_folder, exist_ok=True)

    for mp3_file in mp3_files:
        if file_count == 1000:
            node_count += 1
            file_count = 0
            node_folder = os.path.join(output_folder, f"node{node_count}")
            os.makedirs(node_folder, exist_ok=True)

        dest_path = os.path.join(node_folder, os.path.basename(mp3_file))
        if not os.path.exists(dest_path):
            shutil.copy(mp3_file, dest_path)
            print(f"Copied from {mp3_file} to {dest_path}")
        else:
            print(f"Skipped {mp3_file} (already exists at {dest_path})")

        file_count += 1

    print("All done!")

exist_copy(
    "/leonardo_scratch/large/userexternal/tahmed00/talent-data",
    "/leonardo_scratch/large/userexternal/tahmed00/talent-dataset"
)
