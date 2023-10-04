"""
This script checks directories in `input_packs/`, and will check if mp3 files are present, format all mp3's to be accepted by Waze's file system, and return a valid output pack while returning final pack file size.

In general, these settings help reduce file size:
    Bitrate: Constant 48 kbps
    Channels/Modus: Mono
    Sample frequency: 44100Hz
...but as long as all uploaded files for one pack are < 0.8MB, then we're in business

requires `ffmpeg.exe` in the conversion directory on windows. download from here: https://github.com/BtbN/FFmpeg-Builds/releases

I used `ffmpeg-master-latest-win64-gpl.zip` for my Windows 10 64 bit machine

Android directory of interest: root/data/user/0/com.waze/waze/custom_prompts_temp
"""

import os, shutil
from pydub import AudioSegment
from pydub.utils import mediainfo

AudioSegment.converter = "ffmpeg"
required_voices = []
not_required_voices = []
list_of_input_packs = []
list_of_output_packs = {}

TARGET_BITRATE = 64
SECONDARY_BITRATE = int(float(TARGET_BITRATE)*7.5/8.0)
TERTIARY_BITRATE = int(float(TARGET_BITRATE)*7.0/8.0)
temp_target = TARGET_BITRATE
temp_second = SECONDARY_BITRATE
temp_tert = TERTIARY_BITRATE

# some poorly written code below in hindsight, but it works reliably. if it aint broke?
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
            line = line.strip()
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

def convert_mp3(input_path, output_path, filename):
    audio = AudioSegment.from_file(input_path, format="mp3")

    TARGET_SAMPLE_RATE = 44100
    TARGET_AUDIO_CHANNELS = 1 #mono
    global TARGET_BITRATE
    global SECONDARY_BITRATE
    global TERTIARY_BITRATE 
    global temp_target
    global temp_second
    global temp_tert
    TARGET_VOLUME_INCREASE = 3.5 # decibel increase to get a louder voice (can be attenuated afterwards by the user). I find some voices to be way too quiet at max volume on iOS.

    # Get the bitrate using mediainfo
    metadata = mediainfo(input_path)
    bitrate = int(metadata["bit_rate"]) // 1000  # Convert to kbps
    bitrate_str = str(bitrate) + "k"  # Convert to string with 'k' suffix

    # adjust sample frequency
    if int(audio.frame_rate) > TARGET_SAMPLE_RATE:
        audio = audio.set_frame_rate(44100)

    # check and adjust channels
    if audio.channels != TARGET_AUDIO_CHANNELS:
        audio = audio.set_channels(1)

    # increase volume
    audio = audio + TARGET_VOLUME_INCREASE

    # voice phrases whose quality could be reduced greatly (for space savings on upload)
    rank1_mp3s = ['TickerPoints.mp3', 'Fifth.mp3', 'Sixth.mp3', 'Seventh.mp3']
    # voice phrases who need decent quality, but are not the most entertaining and therefore 2nd rank in terms of quality for space savings
    rank2_mp3s = ['200.mp3',
                  '200meters.mp3',
                  '400.mp3',
                  '400meters.mp3',
                  '800.mp3',
                  '800meters.mp3',
                  '1000meters.mp3',
                  '1500.mp3',
                  '1500meters.mp3',
                  'AndThen.mp3',
                  'ExitLeft.mp3',
                  'ExitRight.mp3',
                  'KeepLeft.mp3',
                  'KeepRight.mp3',
                  'Second.mp3',
                  'First.mp3',
                  'Straight.mp3',
                  'Third.mp3',
                  'TurnLeft.mp3',
                  'TurnRight.mp3'] 
    if filename in rank1_mp3s:
        audio.export(output_path, bitrate=(str(temp_tert) + 'k'), format="mp3")
    elif filename in rank2_mp3s:
        audio.export(output_path, bitrate=(str(temp_second) + 'k'), format="mp3")
    else:
        audio.export(output_path, bitrate=(str(temp_target) + 'k'), format="mp3")
    return bitrate_str

def main():
    global temp_target
    global temp_second
    global temp_tert

    set_mp3_requirements()
    check_input_packs()
    if len(list_of_input_packs) == 0:
        print("No unzipped voice packs found with only *mp3 files. Please check input files")
        exit(0)

    # create an output folder
    make_output_folders()    
    for input_pack in list_of_output_packs.keys():
        success_flag = True
        high_quality_flag = False
        failed_phrases = []
        # preset base paths for each mp3 file
        base_input_path = os.path.join(current_path, local_path)
        base_input_path = os.path.join(base_input_path, 'input_pack')
        base_input_path = os.path.join(base_input_path, input_pack)
        base_output_path = os.path.join(current_path, local_path)
        base_output_path = os.path.join(base_output_path, 'output_pack')
        base_output_path = os.path.join(base_output_path, list_of_output_packs[input_pack])
        num_bytes = 10
        temp_target = TARGET_BITRATE
        temp_second = SECONDARY_BITRATE
        temp_tert = TERTIARY_BITRATE
        fail_flag = False
        while num_bytes > 0.8:# or num_bytes < 0.78:
            for required_file in required_voices:
                # try converting each mp3 file
                try:
                    input_path = os.path.join(base_input_path, required_file)
                    output_path = os.path.join(base_output_path, required_file)
                    bitrate = convert_mp3(input_path, output_path, required_file)
                    if bitrate == '320k':
                        high_quality_flag = True
                except:
                    continue
                    print(f'Failed to convert {input_pack} due to {input_path}')
                    success_flag = False
                    failed_phrases.append(required_file)
                    if required_file != 'TickerPoints.mp3':
                        fail_flag = True
                        break
            if fail_flag:
                break
            #print(f"started at {round(float(get_folder_size(base_input_path))/1000000, 5)}MB")
            num_bytes = round(float(get_folder_size(base_output_path))/1000000, 5)
            break

        # print message and report size for my own knowledge
        num_bytes = round(float(get_folder_size(base_output_path))/1000000, 2)
        if success_flag:
            if high_quality_flag:
                print(f"{input_pack} successfully converted! It is {num_bytes}MB, and was a high quality convert.")
            else:
                print(f"{input_pack} successfully converted! It is {num_bytes}MB.")
        else:
            print(f"{input_pack} semi-converted. It is {num_bytes}MB.\nThe following did not get converted:")
            for phrase in failed_phrases:
                print(f" - {phrase}")

if __name__ == '__main__':
    main()