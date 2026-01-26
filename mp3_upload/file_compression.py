"""
mp3_upload.file_compression

Deterministic MP3 pack compression for Waze-style limits.

Algorithm:
- Preserve pristine originals for every pack
- For each bitrate attempt, regenerate outputs from originals
- Binary-search bitrate so total pack size <= TARGET_FOLDER_SIZE
- Deterministic + monotonic behavior (lower bitrate => smaller size)
"""

import os
import shutil
import time
from multiprocessing import Pool
from pydub import AudioSegment

# ============================
# Compression parameters
# ============================
TARGET_BITRATE = 128              # kbps (upper bound)
MIN_BITRATE = 16                 # kbps (lower bound)
TARGET_SAMPLE_RATE = 44100
TARGET_AUDIO_CHANNELS = 1        # mono
TARGET_VOLUME_INCREASE = 7.0     # dB
TARGET_FOLDER_SIZE = 0.795       # MB

# ============================
# Helpers
# ============================

def get_folder_size(folder_path):
    total = 0
    for root, _, files in os.walk(folder_path):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total / (1024 * 1024)


def convert_mp3(input_path, output_path, bitrate):
    audio = AudioSegment.from_file(input_path, format="mp3")

    if audio.frame_rate != TARGET_SAMPLE_RATE:
        audio = audio.set_frame_rate(TARGET_SAMPLE_RATE)

    if audio.channels != TARGET_AUDIO_CHANNELS:
        audio = audio.set_channels(TARGET_AUDIO_CHANNELS)

    if TARGET_VOLUME_INCREASE:
        audio = audio + TARGET_VOLUME_INCREASE

    audio.export(output_path, format="mp3", bitrate=f"{bitrate}k")


def _convert_worker(args):
    convert_mp3(*args)


# ============================
# Core algorithm
# ============================

def compress_pack(pack_path, output_root):
    pack_name = os.path.basename(pack_path)
    print(f"\n🔄 Processing pack: {pack_name}")

    # Prepare directories
    pristine_path = os.path.join(output_root, f"{pack_name}__ORIGINAL")
    working_path = os.path.join(output_root, pack_name)

    if os.path.exists(pristine_path):
        shutil.rmtree(pristine_path)

    if os.path.exists(working_path):
        shutil.rmtree(working_path)

    shutil.copytree(pack_path, pristine_path)

    def regenerate_at_bitrate(bitrate):
        if os.path.exists(working_path):
            shutil.rmtree(working_path)
        shutil.copytree(pristine_path, working_path)

        tasks = []
        for filename in os.listdir(pristine_path):
            if filename.endswith('.mp3'):
                src = os.path.join(pristine_path, filename)
                dst = os.path.join(working_path, filename)
                tasks.append((src, dst, bitrate))

        with Pool() as pool:
            pool.map(_convert_worker, tasks)

        return get_folder_size(working_path)

    # Initial size check
    initial_size = get_folder_size(pristine_path)
    if initial_size <= TARGET_FOLDER_SIZE:
        shutil.copytree(pristine_path, working_path)
        print(f" - 📦 Already within limit ({initial_size:.2f} MB)")
        return

    # Binary search bitrate
    low = MIN_BITRATE
    high = TARGET_BITRATE
    best_bitrate = TARGET_BITRATE

    while low <= high:
        mid = (low + high) // 2
        size = regenerate_at_bitrate(mid)

        print(f"   🔍 {mid}k → {size:.2f} MB")

        if size > TARGET_FOLDER_SIZE:
            high = mid - 1      # too big → reduce bitrate
        else:
            best_bitrate = mid # valid → try higher quality
            low = mid + 1


    final_size = regenerate_at_bitrate(best_bitrate)

    if final_size >= TARGET_FOLDER_SIZE:
        print(
            f" - ❌ Compression failed: final size {final_size:.2f} MB "
            f"exceeds limit ({TARGET_FOLDER_SIZE:.2f} MB). Removing pack."
        )
        shutil.rmtree(working_path)
        shutil.rmtree(pristine_path)
        return

    print(f" - 🎯 Best bitrate: {best_bitrate}k")
    print(f" - 📦 Final size: {final_size:.2f} MB")

    shutil.rmtree(pristine_path)


# ============================
# Public entry point
# ============================

def compress_mp3_packs(mp3_pack_paths):
    root = os.path.dirname(os.path.abspath(__file__))
    output_root = os.path.join(root, 'compressed_packs')

    if os.path.exists(output_root):
        shutil.rmtree(output_root)
    os.makedirs(output_root)

    print(f"\n📁 Output directory: {output_root}")

    for pack in mp3_pack_paths:
        compress_pack(pack, output_root)

    cleanup_orphaned_pack_dirs(output_root)


# ============================
# Cleanup helpers
# ============================

def cleanup_orphaned_pack_dirs(output_root):
    """
    Remove orphaned or duplicate pack directories such as:
    - "Pack Name 2", "Pack Name 3"
    - "__ORIGINAL", "__ORIGINAL 2"

    These can be left behind if a run exits early or copytree
    collides with an existing directory.
    """
    print("\n🧹 Starting cleanup of orphaned pack directories...")
    time.sleep(12)  # Wait a moment to ensure all file operations are done
    print("🧹 Cleaning orphaned pack directories...")

    entries = os.listdir(output_root)
    to_delete = []

    for name in entries:
        path = os.path.join(output_root, name)

        # Skip non-directories
        if not os.path.isdir(path):
            continue

        # Delete any __ORIGINAL folders
        if "__ORIGINAL" in name:
            to_delete.append(path)
            continue

        # Delete Finder-style duplicates: "Name 2", "Name 3", etc.
        parts = name.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].isdigit():
            base_name = parts[0]
            base_path = os.path.join(output_root, base_name)
            if os.path.exists(base_path):
                to_delete.append(path)

    for path in to_delete:
        print(f" - Removing orphaned folder: {os.path.basename(path)}")
        shutil.rmtree(path, ignore_errors=True)

    if not to_delete:
        print(" - No orphaned folders found")

# ============================
# Example usage
# ============================
if __name__ == '__main__':
    import file_ingestion

    input_directory = os.path.join(os.getcwd(), 'mp3_upload', 'input_packs')
    valid_filenames_file = os.path.join(os.getcwd(), 'mp3_upload', 'valid_waze_filenames.txt')

    packs = file_ingestion.ingest_mp3_packs(input_directory, valid_filenames_file)
    compress_mp3_packs(packs)
