"""
Docstring for mp3_upload.modern_pack_conversion

This script takes all folders in the 'modern_packs' directory and converts them into
compatible input packs in the 'input_packs' directory for further processing.
"""

import os
import shutil
import time

if __name__ == '__main__':
    # show me the packs in modern_packs
    modern_packs_root = os.path.join(os.getcwd(), 'mp3_upload', 'modern_packs')
    input_packs_root = os.path.join(os.getcwd(), 'mp3_upload', 'input_packs')

    modern_pack_dirs = [d for d in os.listdir(modern_packs_root)
                        if os.path.isdir(os.path.join(modern_packs_root, d))]
    print(f"Found {len(modern_pack_dirs)} modern packs to convert.")
    for pack_dir in modern_pack_dirs:
        source_path = os.path.join(modern_packs_root, pack_dir)
        dest_path = os.path.join(input_packs_root, pack_dir)

        print(f"Converting pack: {pack_dir}")
        
        # create or overwrite the destination directory
        if os.path.exists(dest_path):
            print(f" - Destination {dest_path} exists. Removing it first.")
            shutil.rmtree(dest_path)
            time.sleep(1)  # brief pause to ensure deletion is complete

        # iterate over all files in valid_waze_filenames.txt and for each, tell the script where to copy each mp3 from source to destination and what to rename it to
        valid_filenames_file = os.path.join(os.getcwd(), 'mp3_upload', 'valid_waze_filenames.txt')
        with open(valid_filenames_file, 'r') as vf:
            valid_filenames = [line.strip() for line in vf if line.strip()]
        for valid_filename in valid_filenames:
            dest_file_path = os.path.join(dest_path, valid_filename)

            if valid_filename == '200.mp3':
                # inside the source_path, look inside the folder named '200' for '1.mp3' and copy it to dest_file_path
                source_file_path = os.path.join(source_path, '200', '1.mp3')
            elif valid_filename == '200meters.mp3':
                source_file_path = os.path.join(source_path, '200meters', '1.mp3')
            elif valid_filename == '400.mp3':
                source_file_path = os.path.join(source_path, '400', '1.mp3')
            elif valid_filename == '400meters.mp3':
                source_file_path = os.path.join(source_path, '400meters', '1.mp3')
            elif valid_filename == '800.mp3':
                source_file_path = os.path.join(source_path, '800', '1.mp3')
            elif valid_filename == '800meters.mp3':
                source_file_path = os.path.join(source_path, '800meters', '1.mp3')
            elif valid_filename == '1000meters.mp3':
                source_file_path = os.path.join(source_path, '1000meters', '1.mp3')
            elif valid_filename == '1500.mp3':
                source_file_path = os.path.join(source_path, '1500', '1.mp3')
            elif valid_filename == '1500meters.mp3':
                source_file_path = os.path.join(source_path, '1500meters', '1.mp3')
            elif valid_filename.startswith('AndThen'):
                source_file_path = os.path.join(source_path, 'AndThen', '1.mp3')
            elif valid_filename.startswith('ApproachAccident'):
                source_file_path = os.path.join(source_path, 'ApproachAccident', '1.mp3')
            elif valid_filename.startswith('ApproachHazard'):
                source_file_path = os.path.join(source_path, 'ApproachHazard', '1.mp3')
            elif valid_filename.startswith('ApproachRedLightCam'):
                source_file_path = os.path.join(source_path, 'ApproachRedLightCam', '1.mp3')
            elif valid_filename.startswith('ApproachSpeedCam'):
                source_file_path = os.path.join(source_path, 'ApproachSpeedCam', '1.mp3')
            elif valid_filename.startswith('ApproachTraffic'):
                source_file_path = os.path.join(source_path, 'ApproachTraffic', '1.mp3')   
            elif valid_filename.startswith('Arrive'):
                source_file_path = os.path.join(source_path, 'Arrive', '1.mp3')
            elif valid_filename.startswith('ExitLeft'):
                source_file_path = os.path.join(source_path, 'ExitLeft', '1.mp3')
            elif valid_filename.startswith('ExitRight'):
                source_file_path = os.path.join(source_path, 'ExitRight', '1.mp3')
            elif valid_filename.startswith('Fifth'):
                source_file_path = os.path.join(source_path, 'Fifth', '1.mp3')
            elif valid_filename.startswith('First'):
                source_file_path = os.path.join(source_path, 'First', '1.mp3')
            elif valid_filename.startswith('Fourth'):
                source_file_path = os.path.join(source_path, 'Fourth', '1.mp3')
            elif valid_filename.startswith('KeepLeft'):
                source_file_path = os.path.join(source_path, 'KeepLeft', '1.mp3')
            elif valid_filename.startswith('KeepRight'):
                source_file_path = os.path.join(source_path, 'KeepRight', '1.mp3')
            elif valid_filename.startswith('Police'):
                source_file_path = os.path.join(source_path, 'Police', '1.mp3')
            elif valid_filename.startswith('Roundabout'):
                source_file_path = os.path.join(source_path, 'Roundabout', '1.mp3')
            elif valid_filename.startswith('Second'):
                source_file_path = os.path.join(source_path, 'Second', '1.mp3')
            elif valid_filename.startswith('Seventh'):
                source_file_path = os.path.join(source_path, 'Seventh', '1.mp3')
            elif valid_filename.startswith('Sixth'):
                source_file_path = os.path.join(source_path, 'Sixth', '1.mp3')
            elif valid_filename.startswith('StartDrive1'):
                source_file_path = os.path.join(source_path, 'StartDrive', '1.mp3')
            elif valid_filename.startswith('StartDrive2'):
                source_file_path = os.path.join(source_path, 'StartDrive', '2.mp3')
            elif valid_filename.startswith('StartDrive3'):
                source_file_path = os.path.join(source_path, 'StartDrive', '3.mp3')
            elif valid_filename.startswith('StartDrive4'):
                source_file_path = os.path.join(source_path, 'StartDrive', '4.mp3')
            elif valid_filename.startswith('StartDrive5'):
                source_file_path = os.path.join(source_path, 'StartDrive', '5.mp3')
            elif valid_filename.startswith('StartDrive6'):
                source_file_path = os.path.join(source_path, 'StartDrive', '6.mp3')
            elif valid_filename.startswith('StartDrive7'):
                source_file_path = os.path.join(source_path, 'StartDrive', '7.mp3')
            elif valid_filename.startswith('StartDrive8'):
                source_file_path = os.path.join(source_path, 'StartDrive', '8.mp3')
            elif valid_filename.startswith('StartDrive9'):
                source_file_path = os.path.join(source_path, 'StartDrive', '9.mp3')
            elif valid_filename.startswith('Straight'):
                source_file_path = os.path.join(source_path, 'Straight', '1.mp3')
            elif valid_filename.startswith('Third'):
                source_file_path = os.path.join(source_path, 'Third', '1.mp3')
            elif valid_filename.startswith('TickerPoints'):
                source_file_path = os.path.join(source_path, 'TickerPoints', '1.mp3')
            elif valid_filename.startswith('TurnLeft'):
                source_file_path = os.path.join(source_path, 'TurnLeft', '1.mp3')
            elif valid_filename.startswith('TurnRight'):
                source_file_path = os.path.join(source_path, 'TurnRight', '1.mp3')
            elif valid_filename.startswith('uturn'):
                source_file_path = os.path.join(source_path, 'uturn', '1.mp3')
            else:
                print(f" - Warning: No source mapping for {valid_filename}, skipping.")
                continue
            # create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)     
            shutil.copy2(source_file_path, dest_file_path)
            print(f" - Copied {source_file_path} to {dest_file_path}")
            
