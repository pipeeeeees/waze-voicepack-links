"""
This script checks directories in `input_packs/`, and will check if mp3 files are present, format all mp3's to be accepted by Waze's file system, and return a valid output pack while returning final pack file size.

In general, these settings help reduce file size:
    Bitrate: Constant 48 kbps
    Channels/Modus: Mono
    Sample frequency: 44100Hz
...but as long as all uploaded files for one pack are < 0.8MB, then we're in business

requires `ffmpeg.exe` in the conversion directory on windows. download from here: https://github.com/BtbN/FFmpeg-Builds/releases

I used `ffmpeg-master-latest-win64-gpl.zip` for my Windows 64 bit machine

Android directory of interest: root/data/user/0/com.waze/waze/custom_prompts_temp
"""

import os
import shutil
from pydub import AudioSegment
from pydub.utils import mediainfo
from multiprocessing import Pool

TARGET_BITRATE = 64
TARGET_SAMPLE_RATE = 44100
TARGET_AUDIO_CHANNELS = 1   # mono
TARGET_VOLUME_INCREASE = 7.0
TARGET_FOLDER_SIZE = 0.795  # in MB

root = os.path.dirname(os.path.abspath(__file__))
required_files = open(os.path.join(root, 'mp3_filenames.txt'), "r").read().split()

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
    return total_size / (1024 * 1024)  # Convert to MB

def convert_mp3(input_path, output_path, filename, max_bitrate = TARGET_BITRATE):
    audio = AudioSegment.from_file(input_path, format="mp3")

    # Get the bitrate using mediainfo
    metadata = mediainfo(input_path)
    bitrate = int(metadata["bit_rate"]) // 1000  # Convert to kbps

    # Adjust sample rate and channels
    if audio.frame_rate != TARGET_SAMPLE_RATE:
        audio = audio.set_frame_rate(TARGET_SAMPLE_RATE)

    if audio.channels != TARGET_AUDIO_CHANNELS:
        audio = audio.set_channels(TARGET_AUDIO_CHANNELS)

    # Increase volume
    audio = audio + TARGET_VOLUME_INCREASE

    # Check if the bitrate is higher or lower than the max_bitrate
    if bitrate > max_bitrate:
        # If higher, set the bitrate to TARGET_BITRATE
        audio.export(output_path, bitrate=f"{max_bitrate}k", format="mp3")
    else:
        # If lower or equal, keep the original bitrate
        audio.export(output_path, bitrate=f"{bitrate}k", format="mp3")

def convert_mp3_parallel(args):
    input_path, output_path, filename, max_bitrate = args
    convert_mp3(input_path, output_path, filename, max_bitrate)

def main():
    input_pack_path = os.path.join(root, 'input_pack')
    output_pack_path = os.path.join(root, 'output_pack')

    if os.path.exists(output_pack_path):
        shutil.rmtree(output_pack_path)

    os.makedirs(output_pack_path, exist_ok=True)

    for input_folder_name in os.listdir(input_pack_path):
        input_folder = os.path.join(input_pack_path, input_folder_name)

        # Skip processing zip files
        if input_folder_name.endswith('.zip') or input_folder_name.startswith('.'):
            continue

        output_folder = os.path.join(output_pack_path, f"{input_folder_name}_FORMATTED")
        os.makedirs(output_folder)

        # Initialize the bitrate to the TARGET_BITRATE
        current_bitrate = TARGET_BITRATE
        min_bitrate = TARGET_BITRATE // 2  # Start with half of TARGET_BITRATE
        max_bitrate = TARGET_BITRATE * 2  # Double the TARGET_BITRATE initially

        while True:
            pool = Pool()  # Create a multiprocessing pool
            input_files = []

            sub_dirs = os.listdir(input_folder)
            for filename in sub_dirs:
                if filename.endswith('.mp3'):
                    if filename in required_files:
                        input_path = os.path.join(input_folder, filename)
                        output_path = os.path.join(output_folder, filename)

                        # Check if the input file exists
                        if not os.path.exists(input_path):
                            print(f"Input file missing: {input_path}")
                            continue

                        input_files.append((input_path, output_path, filename, current_bitrate))

            # Use multiprocessing pool to convert files in parallel
            pool.starmap(convert_mp3, input_files)
            pool.close()
            pool.join()

            # Calculate the size of the output folder
            output_size = get_folder_size(output_folder)
            #print(f"Converted: {input_folder_name}; Bitrate: {current_bitrate}k; Folder Size: {output_size:.2f} MB")

            # Update the bitrate based on a binary search-like approach
            if (max_bitrate - min_bitrate) <= 1:
                break  # Stop adjusting if the bitrate change is less than or equal to 1k

            if output_size > TARGET_FOLDER_SIZE:
                max_bitrate = current_bitrate
                current_bitrate = (min_bitrate + max_bitrate) // 2
            else:
                min_bitrate = current_bitrate
                current_bitrate = (min_bitrate + max_bitrate) // 2

            #print(f"- Trying {current_bitrate}k to optimize file size and audio quality...")
        print(f"Converted: {input_folder_name}; Bitrate: {current_bitrate}k; Folder Size: {output_size:.2f} MB")


if __name__ == '__main__':
    main()