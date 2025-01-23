import tarfile
import os
import csv
import hashlib

data_folder = "/leonardo_scratch/large/userexternal/tahmed00/data"
output_folder = "/leonardo_scratch/large/userexternal/tahmed00/talent-data"

os.makedirs(output_folder, exist_ok=True)

def safe_filename(name, max_length=100):
    if len(name) > max_length:
        hash_part = hashlib.md5(name.encode()).hexdigest()[:8]
        extension = os.path.splitext(name)[1]
        name = f"{name[:max_length - len(hash_part) - len(extension) - 1]}_{hash_part}{extension}"
    return name

mine_counter = 1

for tar_file_name in os.listdir(data_folder):
    if tar_file_name.endswith(".tar"):
        tar_file_path = os.path.join(data_folder, tar_file_name)
        mine_folder = os.path.join(output_folder, f"MINE{mine_counter}")
        os.makedirs(mine_folder, exist_ok=True)
        csv_file_path = os.path.join(mine_folder, f"MINE{mine_counter}.csv")

        with tarfile.open(tar_file_path, "r") as tar, open(csv_file_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Original Filename", "Revised Filename", "Tarfilename"])

            def tar_filter(member):
                member.name = safe_filename(member.name)
                return member if member.isfile() else None

            members = [tar_filter(m) for m in tar.getmembers()]
            tar.extractall(mine_folder, members=members)

            audio_counter = 0
            for member in members:
                original_filename = member.name
                file_path = os.path.join(mine_folder, original_filename)

                if os.path.exists(file_path):
                    revised_filename = f"audio{audio_counter}"
                    revised_file_path = os.path.join(mine_folder, revised_filename)

                    os.rename(file_path, revised_file_path)

                    json_filename = original_filename.rsplit('.', 1)[0] + ".json"
                    revised_json_filename = revised_filename + ".json"

                    json_file_path = os.path.join(mine_folder, json_filename)
                    revised_json_file_path = os.path.join(mine_folder, revised_json_filename)

                    if os.path.exists(json_file_path):
                        os.rename(json_file_path, revised_json_file_path)

                    csv_writer.writerow([original_filename, revised_filename, tar_file_path])

                    audio_counter += 1

        mine_counter += 1
