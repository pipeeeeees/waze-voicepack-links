import os

def remove_extra_mp3_extension(directory):
    # List all files in the directory
    files = os.listdir(directory)

    # Iterate over each file
    for filename in files:
        # Check if the file ends with '.mp3.mp3'
        if filename.endswith('.mp3.mp3'):
            # Construct the new filename by removing the extra '.mp3'
            new_filename = filename[:-4]
            
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

            print(f"Renamed '{filename}' to '{new_filename}'")

# Replace 'directory_path' with the path to your directory containing the files
directory_path = r'C:\Users\pipee\OneDrive\Documents\GitHub\waze-voicepack-links\conversion\input_pack\Viper Voicepack'
remove_extra_mp3_extension(directory_path)
