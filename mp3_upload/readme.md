# MP3 Upload
This folder contains scripts and tools for uploading MP3 files to a server or cloud storage. There are three main parts to uploading MP3 files:

1. **File Ingestion** - this step involves looking through each pack and checking that each pack contains valid mp3 files. A valid mp3 file in this context is any file that is not corrupted (measured by compatibility with ffmpeg) and matches a name within the `valid-waze-mp3-names.txt` file

![ingestion](https://github.com/pipeeeeees/waze-voicepack-links/blob/main/assets/ingestion.png)

An example of a pack being ingested by the script. In this example, the pack contains at least one valid mp3 file so it is considered valid overall. It is missing some voice files which will be blank in the final upload, but this can be intentional so it's just a warning. All extra mp3 files not in the `valid-waze-mp3-names.txt` file are ignored. 

2. **File Compression** - if needed, the mp3 files will be compressed to meet size requirements for upload. This step is automatically run if the total file size of the pack exceeds the maximum allowed size for upload: 0.8MB. This filesize limit is determined by Waze. Compression is done using ffmpeg with settings that reduce file size while maintaining the highest possible audio quality

![compression](https://github.com/pipeeeeees/waze-voicepack-links/blob/main/assets/compression.png)

An example of a pack being compressed down to below the 0.8MB limit by reducing the bitrate of each mp3 file in the pack (in KB) using a binary search approach, multiprocessing to speed up the process, and checking the total size after each compression iteration

3. **File Upload** - once the files have been ingested and compressed (if needed), upload to Waze's backend is attempted

![upload](https://github.com/pipeeeeees/waze-voicepack-links/blob/main/assets/upload.png)

An example of a successful upload from the script

# How to upload your own mp3 files to make a Waze voicepack link
1. Place your mp3 pack(s) in the `mp3-upload/input-packs/` folder
- each "pack" is a folder containing all of the mp3 files you want to upload together. The folder name will be used as the name of the uploaded voicepack
2. Configure your python environment using the `requirements.txt` file
3. Install ffmpeg on your system if you don't have it already - this is used for file compression and validation
4. Run the `mp3_upload/main.py` script using the configured python environment and follow the progress through each step. If everything is successful, you will see a link to your uploaded voicepack in the console output

# `valid-waze-mp3-names.txt` filenames and their meanings

This file contains a list of valid mp3 filenames that Waze recognizes for voicepacks. Each filename corresponds to a specific voice prompt used in the Waze navigation app. The filenames are structured to indicate the type of prompt, such as directions, alerts, and other navigation-related messages. Here are all the filenames and their meanings:
- `200.mp3` - Prompt for "In 0.1 miles..."
- `200meters.mp3` - Prompt for "In 200 meters..."
- `400.mp3` - Prompt for "In a quarter mile..."
- `400meters.mp3` - Prompt for "In 400 meters..."
- `800.mp3` - Prompt for "In half a mile..."
- `800meters.mp3` - Prompt for "In 800 meters..."
- `1000meters.mp3` - Prompt for "In 1 kilometer..."
- `1500.mp3` - Prompt for "In 1 mile..."
- `1500meters.mp3` - Prompt for "In 1.5 kilometers..."
- `AndThen.mp3` - Prompt for "And then..."
- `ApproachAccident.mp3` - Prompt for "Accident ahead"
- `ApproachHazard.mp3` - Prompt for "Hazard ahead"
- `ApproachRedLightCam.mp3` - Prompt for "Red light camera ahead"
- `ApproachSpeedCam.mp3` - Prompt for "Speed camera ahead"
- `ApproachTraffic.mp3` - Prompt for "Traffic ahead"
- `Arrive.mp3` - Prompt for "You have arrived at your destination"
- `ExitLeft.mp3` - Prompt for "Take the exit on the left"
- `ExitRight.mp3` - Prompt for "Take the exit on the right"
- `Fifth.mp3` - Prompt for "Take the fifth exit"
- `First.mp3` - Prompt for "Take the first exit"
- `Fourth.mp3` - Prompt for "Take the fourth exit"
- `KeepLeft.mp3` - Prompt for "Keep left"
- `KeepRight.mp3` - Prompt for "Keep right"
- `Police.mp3` - Prompt for "Police ahead"
- `Roundabout.mp3` - Prompt for "At the roundabout"
- `Second.mp3` - Prompt for "Take the second exit"
- `Seventh.mp3` - Prompt for "Take the seventh exit"
- `Sixth.mp3` - Prompt for "Take the sixth exit"
- `StartDrive1.mp3` - Prompt for "Starting navigation (1)"
- `StartDrive2.mp3` - Prompt for "Starting navigation (2)"
- `StartDrive3.mp3` - Prompt for "Starting navigation (3)"
- `StartDrive4.mp3` - Prompt for "Starting navigation (4)"
- `StartDrive5.mp3` - Prompt for "Starting navigation (5)"
- `StartDrive6.mp3` - Prompt for "Starting navigation (6)"
- `StartDrive7.mp3` - Prompt for "Starting navigation (7)"
- `StartDrive8.mp3` - Prompt for "Starting navigation (8)"
- `StartDrive9.mp3` - Prompt for "Starting navigation (9)"
- `Straight.mp3` - Prompt for "Continue straight"
- `Third.mp3` - Prompt for "Take the third exit"
- `TickerPoints.mp3` - Prompt for "Rerouting". This file can be omitted as the default chime is good enough. Some people do this to save on file size
- `TurnLeft.mp3` - Prompt for "Turn left"
- `TurnRight.mp3` - Prompt for "Turn right"
- `uturn.mp3` - Prompt for "Make a U-turn"

# How do I add my voicepack link to the main list?
Once you have successfully uploaded your mp3 files and obtained a voicepack link, you can contribute to it by making a fork of this repository and adding your voicepack details to the `helper_files/waze_vps.json` file. After adding your voicepack, you can create a pull request to have it reviewed and potentially merged into the main list. Please ensure that you provide accurate information about the voicepack, including the name, language, and any relevant notes.