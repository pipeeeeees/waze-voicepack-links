# MP3 Upload
This folder contains scripts and tools for uploading MP3 files to a server or cloud storage. There are three main parts to uploading MP3 files:

1. **File Ingestion** - this step involves looking through each pack and checking that each pack contains valid mp3 files. A valid mp3 file in this context is any file that is not corrupted (measured by compatibility with ffmpeg) and matches a name within the `valid-waze-mp3-names.txt` file
2. **File Compression** - if needed, the mp3 files will be compressed to meet size requirements for upload. This step is automatically run if the total file size of the pack exceeds the maximum allowed size for upload: 0.8MB. This filesize limit is determined by Waze. Compression is done using ffmpeg with settings that reduce file size while maintaining the highest possible audio quality
3. **File Upload** - once the files have been ingested and compressed (if needed), upload to Waze's backend is attempted

# How to upload your own mp3 files to make a Waze voicepack link
1. Place your mp3 pack(s) in the `mp3-upload/input-packs/` folder
- each "pack" is a folder containing all of the mp3 files you want to upload together. The folder name will be used as the name of the uploaded voicepack
2. Configure your python environment using the `requirements.txt` file
3. Install ffmpeg on your system if you don't have it already - this is used for file compression and validation
4. Run the `mp3_upload/main.py` script using the configured python environment and follow the progress through each step. If everything is successful, you will see a link to your uploaded voicepack in the console output

# How do I add my voicepack link to the main list?
Once you have successfully uploaded your mp3 files and obtained a voicepack link, you can contribute to it by making a fork of this repository and adding your voicepack details to the `helper_files/waze_vps.json` file. After adding your voicepack, you can create a pull request to have it reviewed and potentially merged into the main list. Please ensure that you provide accurate information about the voicepack, including the name, language, and any relevant notes.