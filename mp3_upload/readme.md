# MP3 Upload
This folder contains scripts and tools for uploading MP3 files to a server or cloud storage. There are three main parts to uploading MP3 files:

1. **File Ingestion** - this step involves looking through each the "packs" within the `mp3-upload/input-packs/` folder and checking that each pack contains valid mp3 files. A valid mp3 file in this context is any file that is not corrupted (measured by compatibility with ffmpeg) and matches a name within the `valid-waze-mp3-names.txt` file
2. **File Compression** - if needed, the mp3 files will be compressed to meet size requirements for upload. This step is automatically run if the total file size of the pack exceeds the maximum allowed size for upload: 0.8MB. This filesize limit is determined by Waze. Compression is done using ffmpeg with settings that reduce file size while maintaining the highest possible audio quality
3. **File Upload** - once the files have been ingested and compressed (if needed), upload to Waze's backend is attempted

# How to Use
1. Place your mp3 pack(s) in the `mp3-upload/input-packs/` folder
- each "pack" is a folder containing all of the mp3 files you want to upload together. The filename of the pack folder will be used as the name of the uploaded voicepack
