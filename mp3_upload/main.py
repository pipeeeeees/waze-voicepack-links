import file_ingestion
import file_compression
import file_upload

import os

if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), 'mp3_upload', 'input_packs')
    output_directory = os.path.join(os.getcwd(), 'mp3_upload', 'compressed_packs')
    valid_filenames_path = os.path.join(os.getcwd(), 'mp3_upload', 'valid_waze_filenames.txt')

    mp3_pack_paths = file_ingestion.ingest_mp3_packs(input_directory, valid_filenames_path)
    file_compression.compress_mp3_packs(mp3_pack_paths)
    file_upload.main()