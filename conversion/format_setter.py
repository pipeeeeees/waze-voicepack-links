import os
import shutil

input_dir = "conversion\pre_inputs"
output_dir = "conversion\pre_outputs"

def convert():
    mp3_filenames = []
    start_drive_flag = False
    with open("conversion\mp3_filenames.txt", "r") as file:
        for line in file:
            filename = line.replace('.mp3','').replace('\n','')
            if "StartDrive" in filename and not start_drive_flag: 
                start_drive_flag = True
                mp3_filenames.append("StartDrive")
            elif "StartDrive" in filename and start_drive_flag:
                pass
            else:
                mp3_filenames.append(line.replace('.mp3','').replace('\n',''))
    #print(mp3_filenames)

    # find all zip files in input_dir and extract them into the input_dir
    for file in os.listdir(input_dir):
        if file.endswith(".zip"):
            shutil.unpack_archive(os.path.join(input_dir, file), input_dir)
    
    # find all folders in input_dir and add them to a list
    folders = []
    for folder in os.listdir(input_dir):
        if os.path.isdir(os.path.join(input_dir, folder)):
            folders.append(folder)

    # clear the output_dir
    shutil.rmtree(output_dir)
    os.mkdir(output_dir)      

    #print(folders)

    # for each folder in the input_dir, find each mp3_filename folder in mp3_filenames somewhere within the input_dir, and print out the files within it
    for folder in folders:
        os.mkdir(os.path.join(output_dir, folder+"_output"))
        for mp3_filename in mp3_filenames:
            for root, dirs, files in os.walk(input_dir + "\\" + folder):
                if mp3_filename in root and mp3_filename == "StartDrive":
                    # make the files `StartDrive1.mp3` through StartDrive9.mp3 by iterating over the files. if there are not enough files to do all 9, then start from the start again
                    for i in range(1,10):
                        if i > len(files):
                            #print(i%len(files))
                            #print(files)
                            #print(root)
                            shutil.copyfile(os.path.join(root, files[i%len(files)]), os.path.join(output_dir, folder+"_output", "StartDrive"+str(i)+".mp3"))
                        else:
                            shutil.copyfile(os.path.join(root, files[i-1]), os.path.join(output_dir, folder+"_output", "StartDrive"+str(i)+".mp3"))
                    break
                elif mp3_filename in root:
                    # if the filename is `1.mp3`, AND it is the only file in the folfer, then copy it to the output_dir under the name `mp3_filename + '.mp3'`
                    if len(files) == 1 and files[0] == "1.mp3":
                        shutil.copyfile(os.path.join(root, files[0]), os.path.join(output_dir, folder+"_output", mp3_filename+".mp3"))
                    # else if there are multiple files, select the file (they are all mp3 files) with the smallest filesize
                    elif len(files) > 1:
                        smallest_file = files[0]
                        for file in files:
                            if os.path.getsize(os.path.join(root, file)) < os.path.getsize(os.path.join(root, smallest_file)):
                                smallest_file = file
                        shutil.copyfile(os.path.join(root, smallest_file), os.path.join(output_dir, folder+"_output", mp3_filename+".mp3"))            
                    break

    
    # finally, check that each folder in the output_dir has all the mp3 files in mp3_filenames
    mp3_filenames = []
    with open("conversion\mp3_filenames.txt", "r") as file:
        for line in file:
            mp3_filenames.append(line.replace('\n',''))

    for folder in os.listdir(output_dir):
        if os.path.isdir(os.path.join(output_dir, folder)):
            for mp3_filename in mp3_filenames:
                if mp3_filename not in os.listdir(os.path.join(output_dir, folder)):
                    print(f"{mp3_filename} not found in {folder}")

    

if __name__ == "__main__":
    convert()