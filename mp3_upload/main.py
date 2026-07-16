import file_ingestion
import file_compression
import file_upload
from ffmpeg_utils import configure_ffmpeg_for_pydub

import os

if __name__ == "__main__":
    configure_ffmpeg_for_pydub()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(script_dir, 'input_packs')
    output_directory = os.path.join(script_dir, 'compressed_packs')
    valid_filenames_path = os.path.join(script_dir, 'valid_waze_filenames.txt')

    mp3_pack_paths = file_ingestion.ingest_mp3_packs(input_directory, valid_filenames_path)
    file_compression.compress_mp3_packs(mp3_pack_paths)
    file_upload.main()