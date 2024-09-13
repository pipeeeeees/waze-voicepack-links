import base64
import requests
import blackboxprotobuf
import login
import uuid
import json
import os
import tarfile

voice_data_proto_buf_type_def = {
    '1001': {
        'type': 'message',
        'message_typedef': {
            '2343': {
                'type': 'message',
                'message_typedef': {
                    '2': {
                        'type': 'message',
                        'message_typedef': {
                            '1': {'type': 'bytes', 'name': ''},
                            '2': {'type': 'bytes', 'name': ''},
                            '5': {'type': 'bytes', 'name': ''},
                            '12': {'type': 'int', 'name': ''}
                        },
                        'name': ''
                    },
                    '3': {'type': 'bytes', 'name': ''}
                },
                'name': ''
            }
        },
        'name': ''
    }
}

voice_data = {
    '1001': {
        '2343': {
            '2': {
                '1': b'packUUID',
                '2': b'NameOfPack',
                '5': b'globalServer',
                '12': 0
            },
            '3': b'TARGZMP3s'
        }
    }
}

metadata_file_data = {
    "uuid": "packUUID",
    "set_name": "NameOfPack",
    "owner": "globalServer",
    "revision": 0,
    "is_uploaded": 2,
    "has_new_version": 0
}

def create_metadata_file(file_path, data):
    try:
        with open(file_path, "w") as meta_file:
            json.dump(data, meta_file)
    except IOError as e:
        print(f"Error creating metadata file: {e}")
        raise

def compress_files(source_dir, archive_name):
    try:
        with tarfile.open(archive_name, "w:gz") as tar:
            for file in os.listdir(source_dir):
                file_path = os.path.join(source_dir, file)
                if os.path.isfile(file_path):
                    tar.add(file_path, arcname=file)
    except Exception as e:
        print(f"Error compressing files: {e}")
        raise


def encode_voice_data(data, proto_buf_type_def):
    try:
        encoded_data = blackboxprotobuf.encode_message(data, proto_buf_type_def)
        base64_encoded = base64.b64encode(encoded_data).decode("utf-8")
        return "ProtoBase64," + base64_encoded
    except Exception as e:
        print(f"Error encoding voice data: {e}")
        raise

def upload_data(url, headers, data, cookies):
    try:
        response = requests.post(url, headers=headers, data=data, cookies=cookies)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Upload failed: {e}")
        raise

def upload(name_of_pack):
    try:
        login_info = login.returnLoginHeader()
        headers = login_info[0]
        global_server = login_info[1]
        cookie_jar = login_info[2]
    except Exception as e:
        print(f"Error retrieving login information: {e}")
        return
    
    pack_uuid = str(uuid.uuid4())
    metadata_file_data.update({
        "uuid": pack_uuid,
        "set_name": name_of_pack,
        "owner": global_server
    })
    voice_data['1001']['2343']['2']['1'] = bytes(pack_uuid, "UTF-8")
    voice_data['1001']['2343']['2']['2'] = name_of_pack.replace("_FORMATTED", "")
    voice_data['1001']['2343']['2']['5'] = global_server

    dir = rf"./conversion/output_pack/{name_of_pack}/"
    if not os.path.exists(dir):
        print("The MP3 directory does not exist.")
        return
    archive_name = "ready.tar.gz"
    compress_files(dir, archive_name)

    try:
        with open(archive_name, "rb") as archive_file:
            voice_data['1001']['2343']['3'] = archive_file.read()
    except IOError as e:
        print(f"Error reading the tar.gz file: {e}")
        return

    built_proto_buf = encode_voice_data(voice_data, voice_data_proto_buf_type_def)
    upload_url = "https://rtproxy-row.waze.com/rtserver/distrib/command"
    try:
        upload_response = upload_data(upload_url, headers, built_proto_buf, cookie_jar)
        print(f"Upload of {name_of_pack} successful.")
    except Exception as e:
        print(f"Upload of {name_of_pack} failed: {e}")
        return

    print(f"https://waze.com/ul?acvp={pack_uuid}")
    print(f"https://voice-prompts-ipv6.waze.com/{pack_uuid}.tar.gz\n")

def main():
    for folder in os.listdir(r"./conversion/output_pack/"):
        upload(folder)

if __name__ == "__main__":
    main()
