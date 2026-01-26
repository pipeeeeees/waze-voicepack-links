"""
Docstring for mp3-upload.file_ingestion

This module handles the ingestion and validation of MP3 files for upload. It
1. Scans the input_pack/ directory for MP3 packs
2. If input packs are found, it validates each MP3 filename against a list of valid Waze MP3 names
3. It also checks that each MP3 file is not corrupted using ffmpeg
4. Prints a report to console and returns a list of valid MP3 packs for further processing
"""

import os
from pydub import AudioSegment

def ingest_mp3_packs(input_directory, valid_filenames_file):
    valid_packs = []
    with open(valid_filenames_file, 'r') as f:
        valid_filenames = set(line.strip() for line in f)


    print(f"\n ** Ingesting MP3 packs from directory: {input_directory} ** ")
    for pack_name in os.listdir(input_directory):
        pack_path = os.path.join(input_directory, pack_name)
        if os.path.isdir(pack_path):
            contains_valid_files = False
            print(f"\n📝 Checking pack: {pack_name}")
            for filename in os.listdir(pack_path):
                if not filename.endswith('.mp3') or filename not in valid_filenames:
                    #print(f"Invalid filename: {filename} in pack: {pack_name}")
                    continue

                file_path = os.path.join(pack_path, filename)
                if not is_mp3_valid(file_path):
                    print(f" - ❌ Corrupted MP3 file: {filename} in pack: {pack_name}")
                    continue

                #print(f" - ✅ Valid MP3 file: {filename} in pack: {pack_name}")
                contains_valid_files = True
                

            if contains_valid_files:
                print(f" - ✅ Valid MP3 pack found: {pack_name}")
                valid_packs.append(pack_path)

            # Now check to see if all files from valid_filenames are present in the pack
            missing_files = valid_filenames - set(os.listdir(pack_path))
            if missing_files:
                print(f" - ⚠️ Missing files in pack {pack_name}: ")
                for missing in missing_files:
                    print(f"   - {missing}")
            else:
                print(f" - 🎉 All files are present in pack {pack_name}")

            # Print total filesize of valid files in the pack
            total_size = 0
            for filename in os.listdir(pack_path):
                if filename in valid_filenames and filename.endswith('.mp3'):
                    file_path = os.path.join(pack_path, filename)
                    total_size += os.path.getsize(file_path)
            total_size_mb = total_size / (1024 * 1024)
            print(f" - 📦 Total size of valid MP3 files in pack {pack_name}: {total_size_mb:.2f} MB")
            #if total_size_mb > 0.8:
                #print(f"  - 📝 Note: This pack requires compression")
            

    return valid_packs

def is_mp3_valid(file_path):
    try:
        audio = AudioSegment.from_file(file_path, format="mp3")
        return True
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), 'mp3_upload', 'input_packs')
    valid_filenames_file = os.path.join(os.getcwd(), 'mp3_upload', 'valid_waze_filenames.txt')

    ingest_mp3_packs(input_directory, valid_filenames_file)