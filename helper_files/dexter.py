import time
import random
import urllib.error
import os
import json

import mp3_language_detector

from os.path import exists
from urllib.request import urlretrieve
import shutil
import zipfile

base_url_dexter = "https://dexter.waze.com/"

dexter_categories = {
    "car": 3,
    "mood": 4,
    "banner_icon": 6,
    "sheet_icon": 7,
    "voice": 8,
    "gallery_promoted_card_icon": 9,
    "gallery_card_icon": 10,
    "setup_cover_image": 11,
    "gallery_car_icon": 13
}

def construct_path(url, category):
    filename = url.split('/')[-1]
    path = category + "/" + filename.rstrip('\n')
    return path

def main(download_all=False):
    category_name = "voice"  # change here to download other categories
    category_id = dexter_categories[category_name]

    # if `voice_index.json` does not exist in helper_files/, create the file in helper_files/
    helper_files_dir = "helper_files"
    voice_index_file = os.path.join(helper_files_dir, "dexter_voice_index.json")
    if not exists(voice_index_file):
        os.makedirs(helper_files_dir, exist_ok=True)
        with open(voice_index_file, "w") as f:
            f.write("[]")

    # if `blanks_index.json` does not exist in helper_files/, create the file in helper_files/
    blanks_index_file = os.path.join(helper_files_dir, "dexter_voice_blanks_index.json")
    if not exists(blanks_index_file):
        os.makedirs(helper_files_dir, exist_ok=True)
        with open(blanks_index_file, "w") as f:
            f.write("[]")

    for i in range(842, 11000):
        url = f"{base_url_dexter}{category_id}/{i}.zip"
        path = construct_path(url, category_name + "s")  # plurals

        with open(voice_index_file, "r") as f:
            voice_data = json.load(f)

        with open(blanks_index_file, "r") as f:
            blanks_data = json.load(f)

        # if i is smaller thhan the largest index in voice_data, continue
        if voice_data and i <= max(item["index"] for item in voice_data):
            continue

        # Check if this pack was already extracted to downloaded_packs/<i>
        extracted_dir = os.path.join(helper_files_dir, "downloaded_packs", str(i))
        if exists(extracted_dir):
            continue

        else:
            print(f"Downloading: {i}.zip")
            try:
                # ensure download directory exists
                os.makedirs(os.path.join(helper_files_dir, "downloaded_packs"), exist_ok=True)
                # urlretrieve to helper_files/downloaded_packs/
                zip_path = os.path.join(helper_files_dir, "downloaded_packs", f"{i}.zip")
                urlretrieve(url, zip_path)
                print(f"Downloaded: {i}.zip")
                # unzip the file in place (cross-platform)
                extracted_path = os.path.join(helper_files_dir, 'downloaded_packs', str(i))
                os.makedirs(extracted_path, exist_ok=True)
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    zf.extractall(extracted_path)
                print(f"Unzipped: {i}.zip")

                # deduce primary language of the unzipped pack
                path_to_zip = os.path.join(helper_files_dir, "downloaded_packs", f"{i}", "Voice")
                primary_language = mp3_language_detector.deduce_primary_language(path_to_zip, verbose=True)
                print(f"Primary Language: {primary_language}")

                with open(voice_index_file, "r+") as f:
                    data = json.load(f)
                    data.append({"index": i, "language": primary_language, "name": ""})
                    data = sorted(data, key=lambda x: x["index"]) 
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()

                # delete the zip file after successful download and extraction
                os.remove(os.path.join(helper_files_dir, "downloaded_packs", f"{i}.zip"))

                # if the primary language is not "en", delete the extracted folder
                if primary_language != "en" and not download_all:
                    try:
                        shutil.rmtree(extracted_path)
                        print(f"Deleted non-English pack: {i}.zip")
                    except FileNotFoundError:
                        pass
                    
            # if there is nothing to download just log it in the json
            except urllib.error.URLError as e:
                print(f"Error downloading from {url}: {e}")
                # Append to blanks_index.json. if the index already exists, overwrite it. and sort the json by index before saving
                with open(blanks_index_file, "r+") as f:
                    data = json.load(f)
                    # check if index already exists
                    existing_indices = [item["index"] for item in data]
                    if i not in existing_indices:
                        data.append({"index": i})
                    data = sorted(data, key=lambda x: x["index"])
                    f.seek(0)
                    json.dump(data, f, indent=4)

            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        # Generate a random sleep duration between 0.25 and 1.5 seconds
        sleep_duration = random.uniform(0.25, 0.75)

        # Sleep for the generated duration
        time.sleep(sleep_duration)


if __name__ == "__main__":
    main(download_all=False)