import json
import os

with open('helper_files/waze_vps.json', 'r') as f:
    waze_vps_json = f.read()

SHARE_BASE_URI = "https://waze.com/ul?acvp="
FILES_BASE_URI = "https://voice-prompts-ipv6.waze.com/"
FILES_URI_SUFFIX = ".tar.gz"

def generate_official_voicepacks_markdown_table(waze_vps_json) -> str:
    waze_vps = json.loads(waze_vps_json)
    official_voicepacks = waze_vps.get("Official Voicepacks", [])
    
    markdown_table = "| Name | Link | Language | mp3 files | Notes |\n"
    markdown_table += "|------|----------|----------|-----------|-------|\n"
    
    for vp in official_voicepacks:
        name = vp.get("name", "N/A")
        language = vp.get("language", "N/A")
        uuid = vp.get("uuid", "N/A")
        notes = vp.get("notes", "")
        share_link = f"{SHARE_BASE_URI}{uuid}"
        files_link = f"{FILES_BASE_URI}{uuid}{FILES_URI_SUFFIX}"
        markdown_table += f"| {name} | [Link]({share_link}) | {language} | [mp3 files]({files_link}) | {notes} |\n"
    
    return markdown_table

def generate_community_voicepacks_markdown_table(waze_vps_json) -> str:
    waze_vps = json.loads(waze_vps_json)
    community_voicepacks = waze_vps.get("Community Voicepacks", [])
    
    markdown_table = "| Name | Link | Language | mp3 files | Notes |\n"
    markdown_table += "|------|----------|----------|-----------|-------|\n"
    
    for vp in community_voicepacks:
        name = vp.get("name", "N/A")
        language = vp.get("language", "N/A")
        uuid = vp.get("uuid", "N/A")
        share_link = f"{SHARE_BASE_URI}{uuid}"
        files_link = f"{FILES_BASE_URI}{uuid}{FILES_URI_SUFFIX}"
        # if the vp has the "author" field, include it in the notes
        author = vp.get("author", "")
        author_link = vp.get("author_link", "")
        json_notes = vp.get("notes", "")
        if author:
            if author_link:
                notes = f"By [{author}]({author_link})"
            else:
                notes = f"By {author}"
        else:
            notes = ""
        if json_notes:
            notes += f" {json_notes}"

        markdown_table += f"| {name} | [Link]({share_link}) | {language} | [mp3 files]({files_link}) | {notes} |\n"
    
    return markdown_table

intro_string = """
# Waze Voicepack Links

Welcome to the largest public repository of Waze custom GPS voices on the internet. This project was created in an effort to consolidate all shareable Waze voice links into one list that can receive continuous community updates (rather than out-of-date reddit posts or ad-laden website articles). 

## How to Download a Voicepack

1. On your mobile device, have the Waze app installed.
2. On the same mobile device, click on one of the links below beside the voicepack title of your choice.
3. Select the voice of your choosing in the Waze app by going to `My Waze` > Tap on the white button with three lines in the top left corner > `Settings` > `Voice & Sound` > `Waze voice` > Tap on the new voice.

# Waze Official Voice List

This list contains current and former contracted celebrities and voice actors who at one point had their voices officially on the Waze App. Their voices have since been saved and converted into user-made custom voice packs with shareable links of varying quality. 
"""

community_list_intro_string = """
# Waze Community Voice List

This list contains user-created voice packs made by the Waze community. These voices are often created using the in-app microphone recording feature or by uploading `.mp3` files to Waze's servers. The quality of these voice packs can vary greatly depending on the source of the audio files used to create them.
"""

outro_string = """
## Have mp3 files?
I can create voice packs from `.mp3` files. If you have `.mp3` files for voices not yet on this list, please open an issue and share the files. Please format the filenames as seen [here](https://github.com/pipeeeeees/waze-voicepack-links/blob/main/conversion/mp3_filenames.txt). 
- Note that `200.mp3` is the callout for 0.1 miles, `400.mp3` for a quarter of a mile, `800.mp3` for half a mile, and `1500.mp3` for a mile. `TickerPoints.mp3` is for rerouting (does not need to be provided if the default chime is OK with you). The rest should be self evident.

The advantage of using files to create packs rather than using the in-app microphone is the preservation of audio quality. By default, Waze heavily compresses the in-app recordings making them sound muffled. While the file upload method may also involve some file compression on the server side, the audio quality is far superior to the in-app recording method. 

## Stance on A.I. Generated Voicepacks
Given the proliferation of A.I. voice generation tools in the hands of the public, there is an influx of A.I. generated Waze navigation voicepacks. These are often created without the explicit permission of the person or IP owner these voices belong to. This is a clear concern.

The purpose of this repository is to act as an archive of the internet's Waze voicepacks while providing tools to create permanent shareable Waze voicepack links. As the creator of this repository, I do not own the voice content stored on Waze's servers - only the files and text in this repository. To address the ethical concerns surrounding A.I. generated voicepacks, I have established the following guidelines:
- Any known A.I. voicepacks will be labeled as such in the 'Title' column of the lists above. If you find a voice in the lists above to be A.I. generated but not correctly labeled, please open an issue or a pull request with the corrected title.
- If the voice actor or IP owner for an A.I. generated voicepack in the list above would like to have a pack removed from this list, the request will be honored. Please open a new issue with the request and I or a contributor will get back to you. 

"""

def generate_readme(waze_vps_json):
    official_table = generate_official_voicepacks_markdown_table(waze_vps_json)
    community_table = generate_community_voicepacks_markdown_table(waze_vps_json)

    readme_content = f"{intro_string}\n{official_table}\n{community_list_intro_string}\n{community_table}\n{outro_string}"
    
    # generate README.md file in cwd / helper_files directory (remove old one if it exists)
    cwd = os.getcwd()
    readme_path = os.path.join(cwd, 'helper_files/README.md')
    if os.path.exists(readme_path):
        os.remove(readme_path)
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    



if __name__ == "__main__":
    
    #official_table = generate_official_voicepacks_markdown_table(waze_vps_json)
    #community_table = generate_community_voicepacks_markdown_table(waze_vps_json)

    generate_readme(waze_vps_json)