import os
import shutil

# Define the input and output directories
input_dir = "conversion\pre_inputs"
output_dir = "conversion\pre_outputs"

def copy_file_with_new_name(input_file, new_file_name, output_dir):
    # Create the output file path by joining the output directory and the new file name
    output_file = os.path.join(output_dir, new_file_name)
    # Copy the file to the output directory with the new name
    shutil.copy2(input_file, output_file)

# Remove everything out of the pre_outputs folder
for root, dirs, files in os.walk(output_dir, topdown=False):
    for file in files:
        file_path = os.path.join(root, file)
        os.remove(file_path)
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        shutil.rmtree(dir_path)

first_choice = ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','KeepLeft','KeepRight','1000','uturn','ExitLeft','ExitRight']
# Iterate through subfolders in the input directory
for root, dirs, files in os.walk(input_dir):
    # Create corresponding subfolders in the output directory
    output_subfolder = os.path.join(output_dir, os.path.relpath(root, input_dir))
    file_name = 'h'

    if root == r'conversion\pre_inputs':
        os.makedirs(output_subfolder, exist_ok=True)
    elif len(root.split('\\')) == 3:
        os.makedirs(output_subfolder, exist_ok=True)
    elif len(root.split('\\')) == 4:
        file_name = root.split("\\")[-1] + '.mp3'
        if len(files) == 1 and files[0] == '1.mp3':
            copy_file_with_new_name(root + '\\' + '1.mp3', file_name, output_dir + '\\' + root.split("\\")[2])
        elif root.split("\\")[-1] in first_choice:
            copy_file_with_new_name(root + '\\' + '1.mp3', file_name, output_dir + '\\' + root.split("\\")[2])
        elif root.split("\\")[-1] == 'StartDrive':
            if len(files) == 9:
                for i in range(9):
                    copy_file_with_new_name(root + '\\' + files[i], 'StartDrive' + str(i+1) + '.mp3', output_dir + '\\' + root.split("\\")[2])
            else:
                taken = []
                for i in range(9):
                    phrase = root.split("\\")[-1]
                    title = root.split("\\")[-2]
                    print(f'\nFor {phrase} ({title}), pick from the following:')
                    num = 1
                    for file in files:
                        if num not in taken:
                            print(f'\t{num}: {file}')
                        num += 1
                    value = int(input('   Pick your choice: '))
                    copy_file_with_new_name(root + '\\' + files[value-1], 'StartDrive' + str(i+1) + '.mp3', output_dir + '\\' + root.split("\\")[2])
                    taken.append(value)
        else:
            phrase = root.split("\\")[-1]
            title = root.split("\\")[-2]
            print(f'\nFor {phrase} ({title}), pick from the following:')
            num = 1
            for file in files:
                print(f'\t{num}: {file}')
                num += 1
            value = int(input('   Pick your choice: '))
            copy_file_with_new_name(root + '\\' + files[value-1], file_name, output_dir + '\\' + root.split("\\")[2])
