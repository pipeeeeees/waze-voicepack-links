import os
import subprocess
from pydub import AudioSegment

def check_ffmpeg():
    # Check if ffmpeg is available in the system
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("ffmpeg is installed and available.")
        return True
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("ffmpeg is not installed or not in the system path.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("ffmpeg is installed but returned an error when queried.")
        return False

def generate_dummy_wav():
    # Generate a dummy sample.wav file
    sample_wav = "sample.wav"
    if not os.path.exists(sample_wav):
        # Create a silent audio segment with duration 1 second
        silent_segment = AudioSegment.silent(duration=1000)
        # Export the silent segment as WAV file
        silent_segment.export(sample_wav, format="wav")
        print(f"Dummy {sample_wav} generated.")
    else:
        print(f"{sample_wav} already exists.")

def cleanup(files):
    # Remove the generated files
    for file in files:
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except FileNotFoundError:
            print(f"File not found: {file}")
            pass

def convert_audio(input_file, output_file, format='mp3'):
    # Run a simple test to convert an audio file to the specified format
    try:
        subprocess.run(['ffmpeg', '-i', input_file, output_file], check=True)
        print(f"Conversion successful: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")

if __name__ == "__main__":
    # Check for ffmpeg
    if check_ffmpeg():
        # Generate dummy sample.wav
        generate_dummy_wav()

        # Example usage: Convert sample.wav to sample_converted.mp3
        input_file = "sample.wav"
        output_file = "sample_converted.mp3"
        convert_audio(input_file, output_file)

        # Cleanup generated files
        cleanup([input_file, output_file])
