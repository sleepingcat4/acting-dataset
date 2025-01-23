import tarfile
import os
import csv
import hashlib

data_folder = "/leonardo_scratch/large/userexternal/tahmed00/data"
output_folder = "/leonardo_scratch/large/userexternal/tahmed00/talent-data"

os.makedirs(output_folder, exist_ok=True)

def hash_filename(name):
    return hashlib.sha256(name.encode()).hexdigest()

mine_counter = 1

for tar_file_name in os.listdir(data_folder):
    if tar_file_name.endswith(".tar"):
        tar_file_path = os.path.join(data_folder, tar_file_name)
        mine_folder = os.path.join(output_folder, f"MINE{mine_counter}")
        os.makedirs(mine_folder, exist_ok=True)
        csv_file_path = os.path.join(mine_folder, f"MINE{mine_counter}.csv")

        with tarfile.open(tar_file_path, "r") as tar, open(csv_file_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "Original AudioFilename",
                "Hashed AudioFilename",
                "Original JSONFilename",
                "Hashed JSONFilename"
            ])

            members = [m for m in tar.getmembers() if m.isfile()]
            file_mappings = []

            for member in members:
                original_name = os.path.basename(member.name)
                hashed_name = hash_filename(original_name)
                extension = os.path.splitext(original_name)[1]
                hashed_name_with_ext = f"{hashed_name}{extension}"

                member.name = hashed_name_with_ext

                file_mappings.append({
                    "original_name": original_name,
                    "hashed_name": hashed_name_with_ext,
                    "extension": extension,
                })

            tar.extractall(mine_folder, members=members)

            audio_files = [f for f in file_mappings if f["extension"] in [".mp3", ".wav", ".flac"]]
            json_files = [f for f in file_mappings if f["extension"] == ".json"]

            for audio_file in audio_files:
                audio_original = audio_file["original_name"]
                audio_hashed = audio_file["hashed_name"]

                matching_json = next(
                    (j for j in json_files if j["original_name"].startswith(os.path.splitext(audio_original)[0])),
                    None
                )

                json_original = matching_json["original_name"] if matching_json else ""
                json_hashed = matching_json["hashed_name"] if matching_json else ""

                csv_writer.writerow([
                    audio_original,
                    audio_hashed,
                    json_original,
                    json_hashed
                ])

        mine_counter += 1
