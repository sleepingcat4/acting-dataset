import os
import csv

def generate_paths(src_dir, csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['FilePath'])  # Write header

        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.mp3'):
                    writer.writerow([os.path.join(root, file)])
    
    print(f"CSV file created at: {csv_path}")

