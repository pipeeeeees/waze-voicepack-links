"""
checks directories in `input_packs/`, and will check if mp3 files are present, format all mp3's to be accepted by Waze's file system, and return a valid output pack

Bitrate: Constant 48 kbps
Channels/Modus: Mono
Sample frequency: 44100Hz

requires `ffmpeg.exe` in the conversion directory on windows. download from here: https://github.com/BtbN/FFmpeg-Builds/releases

I used `ffmpeg-master-latest-win64-gpl.zip` for my windows machine

1.6MB total output is the absolute max it seems...
"""

import os, shutil
from pydub import AudioSegment
from pydub.utils import mediainfo


AudioSegment.converter = "ffmpeg"
required_voices = []
not_required_voices = []
list_of_input_packs = []
list_of_output_packs = {}

#set OS independent relative paths and slash flags
#did this to work locally on my mac, but ffmpeg.exe was too hard to find a mac equivalent... largely due to laziness... this effort was wasted in the end but ill keep it here as I am lazy. I think os has functions to handle this anyway...
current_path = os.getcwd()
if '\\' in current_path:
    path_slash = '\\'
    windows_os_flag = True
    path_ending = current_path.split('\\')[-1]
    if path_ending == 'conversion':
        local_path = ''
    else:
        local_path = 'conversion\\'
elif '/' in current_path:
    path_slash = '/'
    windows_os_flag = False
    path_ending = current_path.split('/')[-1]
    if path_ending == 'conversion':
        local_path = ''
    else:
        local_path = 'conversion/'
else:
    print('something went wrong')
    exit(0)

def get_folder_size(folder_path):
    """
    Get the size of a folder in bytes.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        int: The size of the folder in bytes.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def set_mp3_requirements():
    global required_voices
    global not_required_voices

    try:
        file_path = "conversion/prompt_names.txt"
    except:
        file_path = "prompt_names.txt"

    with open(file_path, 'r') as file:
        required_flag = True
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces, if needed
            
            if line == '% Required':
                required_flag = True
                continue
            elif line == '% Not Needed':
                required_flag = False
                continue
            elif line == '':
                break
            if required_flag == True:
                required_voices.append(line)
            else:
                not_required_voices.append(line)

def check_input_packs():
    global list_of_input_packs

      # Flag to track if all files in the folder are .mp3 files

    input_pack_path = local_path + 'input_pack'

    file_list = os.listdir(input_pack_path)
    for file_name in file_list:
        if '.' not in file_name:
            mp3_only = True
            specific_path = input_pack_path + path_slash + file_name
            folder_list = os.listdir(specific_path)
            for file in folder_list:
                if not file.lower().endswith('.mp3'):
                    mp3_only = False
                    break
            if mp3_only:
                list_of_input_packs.append(file_name)

def make_output_folders():
    # delete the output folder
    output_file_path = local_path + path_slash + 'output_pack'
    if os.path.exists(output_file_path):
        shutil.rmtree(output_file_path)

    # create the output folder and subfolders
    output_file_path = output_file_path + path_slash
    for input_folder_name in list_of_input_packs:
        if not os.path.exists(output_file_path + input_folder_name + '_FORMATTED'):
            os.makedirs(output_file_path + input_folder_name + '_FORMATTED')
            list_of_output_packs[input_folder_name] = input_folder_name + '_FORMATTED'

def convert_mp3(input_path, output_path):
    """
    specifications for audio quality that is accepted by the Waze app can be found here: https://www.reddit.com/r/waze/comments/wiq9iq/comment/ijdki4p/?utm_source=share&utm_medium=web2x&context=3
    
    extremely useful, u/BosterMaiti
    """
    # load the input MP3 file
    audio = AudioSegment.from_file(input_path, format="mp3")

    TARGET_SAMPLE_RATE = 44100
    TARGET_AUDIO_CHANNELS = 1 #mono
    TARGET_BITRATE = '64k'

    ## SAMPLE FREQUENCY CONVERSION
    if int(audio.frame_rate) != TARGET_SAMPLE_RATE:
        old_audio_frame_rate = int(audio.frame_rate)
        # Modify the sample frequency to 44100Hz
        audio = audio.set_frame_rate(44100)
        #print(f"Sample frequency modified to 44100Hz from {old_audio_frame_rate}Hz.")

    ## CHANNELS CONVERSION
    if audio.channels != TARGET_AUDIO_CHANNELS:
        # Convert stereo or other formats to mono
        old_audio_channels = audio.channels
        audio = audio.set_channels(1)
        #print(f"Audio converted to mono from {old_audio_channels}.")

    #output_file_path = os.path.join(output_path, "output.mp3")

    audio.export(output_path, bitrate=TARGET_BITRATE, format="mp3")
    #print("Modified audio saved to:", output_path)

def main():
    # pull Waze mp3 file requirements from `prompt_names.txt`
    set_mp3_requirements()

    # check the input_pack folder
    check_input_packs()
    if len(list_of_input_packs) == 0:
        print("No unzipped voice packs found with only *mp3 files. Please check input files")
        exit(0)

    # create an output folder
    make_output_folders()
    
    # go thru each folder and convert each
    for input_pack in list_of_output_packs.keys():
        # preset base paths for each mp3 file
        base_input_path = os.path.join(current_path, local_path)
        base_input_path = os.path.join(base_input_path, 'input_pack')
        base_input_path = os.path.join(base_input_path, input_pack)
        base_output_path = os.path.join(current_path, local_path)
        base_output_path = os.path.join(base_output_path, 'output_pack')
        base_output_path = os.path.join(base_output_path, list_of_output_packs[input_pack])
        for required_file in required_voices:
            # try converting each mp3 file
            try:
                input_path = os.path.join(base_input_path, required_file)
                output_path = os.path.join(base_output_path, required_file)
                convert_mp3(input_path, output_path)
            except:
                print(f'Failed to convert {input_pack} due to {input_path}')
                print('This could be because this file does not exist in the input file folder.')
                break
        num_bytes = round(float(get_folder_size(base_output_path))/1000000, 2)

        print(f"{input_pack} successfully converted! It is {num_bytes}MB.")

if __name__ == '__main__':
    main()