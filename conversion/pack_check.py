"""
checks directories in `input_packs/`, and will check if files are present, formatted correctly, and return a valid output pack

Bitrate: Constant 64 kbps
Channels/Modus: Mono
Sample frequency: 44100Hz

"""

import os, shutil
from pydub import AudioSegment
AudioSegment.converter = "ffmpeg"

required_voices = []
not_required_voices = []
list_of_input_packs = []
list_of_output_packs = {}

#set OS independent relative paths and slash flags
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
    # Load the input MP3 file
    audio = AudioSegment.from_file(input_path, format="mp3")

    # Check the current sample frequency
    sample_frequency = audio.frame_rate
    print("Current sample frequency:", sample_frequency, "Hz")

    # Check if the sample frequency needs to be modified
    if sample_frequency != 44100:
        # Modify the sample frequency to 44100Hz
        audio = audio.set_frame_rate(44100)
        print("Sample frequency modified to 44100Hz.")

    output_file_path = os.path.join(output_path, "output.mp3")

    audio.export(r'C:\Users\pipee\Desktop\waze-voicepack-links\conversion\output_pack\vp_eng_cat_voice_FORMATTED\output1.mp3', format="mp3")
    print("Modified audio saved to:", output_file_path)

    return True

def main():
    global required_voices
    global not_required_voices
    global list_of_input_packs

    # pull Waze mp3 file requirements from `prompt_names.txt`
    set_mp3_requirements()

    # check the input_pack folder
    check_input_packs()
    if len(list_of_input_packs) == 0:
        print("No unzipped voice packs found with only *mp3 files. Please check input files")
        exit(0)

    # create an output folder
    make_output_folders()
    
    # TEST: successfully format an mp3 in bitrate, channels, and sample freq
    convert_mp3(r'C:\Users\pipee\Desktop\waze-voicepack-links\conversion\input_pack\vp_eng_cat_voice\200.mp3', local_path + 'output_file' + path_slash + 'vp_eng_cat_voice_FORMATTED')

if __name__ == '__main__':
    main()