"""
checks directories in `input_packs/`, and will check if files are present, formatted correctly, and return a valid output pack

Bitrate: Constant 64 kbps
Channels/Modus: Mono
Sample frequency: 44100Hz

"""

import os

required_voices = []
not_required_voices = []
list_of_input_packs = []

#set OS independent relative paths and slash flags
current_path = os.getcwd()
if '\\' in current_path:
    windows_os_flag = True
    path_ending = current_path.split('\\')[-1]
    if path_ending == 'conversion':
        local_path = ''
    else:
        local_path = 'conversion\\'
elif '/' in current_path:
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

def check_input_packs(folder_path):
    mp3_only = True  # Flag to track if all files in the folder are .mp3 files
 
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.lower().endswith('.mp3'):
                mp3_only = False
                break
    
    if mp3_only:
        folder_name = os.path.basename(folder_path)
        list_of_input_packs.append(folder_name)

def process_input_packs(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            check_input_packs(item_path)

def main():
    global required_voices
    global not_required_voices

    set_mp3_requirements()


    return

if __name__ == '__main__':
    main()