"""
Docstring for mp3_upload.file_upload

This module handles the uploading of compressed MP3 packs to the Waze server. It
1. Scans the compressed_packs/ directory for MP3 packs
2. Authenticates with Waze using Protocol Buffer-based login
3. Uploads each MP3 pack to the Waze server using their API
4. Logs the upload status and any errors encountered during the process

"""

import base64
import requests
import blackboxprotobuf
import uuid
import json
import os
import sys
import time
import tarfile


# ============================================================================
# Authentication Functions
# ============================================================================

def decodeHexProtoBUF(hexString):
    """Decode hex-encoded Protocol Buffer to JSON."""
    message, bufType = blackboxprotobuf.protobuf_to_json(base64.b16decode(hexString, True))
    return json.loads(message)


def encodeToProtoBase64(jsonData, protoType):
    """Encode JSON data to Protocol Buffer and Base64."""
    return 'ProtoBase64,' + str(base64.b64encode(blackboxprotobuf.encode_message(jsonData, protoType)), 'utf-8')


def returnLoginHeader():
    """Authenticate with Waze and return headers, global server, and cookie jar."""
    UUID1 = str(uuid.uuid4())
    UUID2 = str(uuid.uuid4())
    UUID3 = str(uuid.uuid4())

    mainPOSTTypeDef = {'1001': {'type': 'message', 'message_typedef': {'2184': {'type': 'message', 'message_typedef': {'1': {'type': 'int', 'name': ''}, '3': {'type': 'bytes', 'name': ''}, '5': {'type': 'bytes', 'name': ''}, '6': {'type': 'bytes', 'name': ''}, '11': {'type': 'bytes', 'name': ''}, '16': {'type': 'bytes', 'name': ''}, '17': {'type': 'bytes', 'name': ''}, '18': {'type': 'int', 'name': ''}, '19': {'type': 'int', 'name': ''}, '22': {'type': 'message', 'message_typedef': {'1': {'type': 'message', 'message_typedef': {'1': {'type': 'bytes', 'name': ''}, '2': {'type': 'bytes', 'name': ''}}, 'name': ''}}, 'name': ''}, '24': {'type': 'message', 'message_typedef': {'1': {'type': 'int', 'name': ''}, '2': {'type': 'int', 'name': ''}, '3': {'type': 'int', 'name': ''}}, 'name': ''}, '25': {'type': 'bytes', 'name': ''}, '26': {'type': 'bytes', 'name': ''}, '28': {'type': 'int', 'name': ''}}, 'name': ''}}, 'name': ''}}
    secondPOSTTypeDef2 = {'1001': {'type': 'message', 'message_typedef': {'2219': {'type': 'message', 'message_typedef': {}, 'name': ''}}, 'name': ''}}
    thirdPOSTTypeDef2 = {'1001': {'type': 'message', 'message_typedef': {'2744': {'type': 'message', 'message_typedef': {'1': {'type': 'message', 'message_typedef': {'1': {'type': 'bytes', 'name': ''}, '2': {'type': 'bytes', 'name': ''}}, 'name': ''}, '3': {'type': 'int', 'name': ''}, '4': {'type': 'int', 'name': ''}, '5': {'type': 'int', 'name': ''}}, 'name': ''}}, 'name': ''}}
    thirdPOSTTypeDef3 = {'1001': {'type': 'message', 'message_typedef': {'2108': {'type': 'message', 'message_typedef': {'1': {'type': 'bytes', 'name': ''}, '2': {'type': 'int', 'name': ''}}, 'name': ''}}, 'name': ''}}

    mainPOSTData = {"1001":{"2184":{"1":234,"3":"4.106.0.1","5":"Waydroid","6":"WayDroid x86_64 Device","11":"11-SDK30","16":"en","17":"bb4e-UUID1","18":50,"19":1,"22":{"1":{"1":"uid_enabled","2":"true"}},"24":{"1":2,"2":1920,"3":1137},"25":"en","26":"e7a0-UUID2","28":"EPOCHTIME"}}}
    secondPOSTData2 = {"1001":{"2219":{}}}
    thirdPOSTData2 = {"1001":{"2744":{"1":{"1":"worldDATA","2":"RANDSTRINGDATA"},"3":0,"4":0,"5":1}}}
    thirdPOSTData3 = {"1001":{"2108":{"1":"fdc9-UUID3","2":1}}}

    sequenceNumberHeader = 1

    epochTime = int(time.time())

    mainPOSTData["1001"]["2184"]["28"] = epochTime
    mainPOSTData["1001"]["2184"]["17"] = UUID1
    mainPOSTData["1001"]["2184"]["26"] = UUID2

    firstPOSTData = encodeToProtoBase64(mainPOSTData, mainPOSTTypeDef)
    firstPOSTData = firstPOSTData + "\n" + "GetGeoServerConfig,world,T"

    headerss = {"user-agent": "4.106.0.1", "sequence-number": str(sequenceNumberHeader), "x-waze-network-version": "3", "x-waze-wait-timeout": "3500"}
    cookieJar = requests.cookies.RequestsCookieJar()

    firstPOSTResponse = requests.post("https://rt.waze.com/rtserver/distrib/login", data=firstPOSTData, headers=headerss, cookies=cookieJar)
    if firstPOSTResponse.status_code != 200:
        print("Failed first POST Request.")
        print("Server response: " + str(firstPOSTResponse.content))
        sys.exit()

    sequenceNumberHeader += 1

    epochTime = int(time.time())
    mainPOSTData["1001"]["2184"]["28"] = epochTime
    secondPOSTData1 = encodeToProtoBase64(mainPOSTData, mainPOSTTypeDef)
    secondPOSTData2 = encodeToProtoBase64(secondPOSTData2, secondPOSTTypeDef2)
    secondPOSTData = secondPOSTData1 + "\n" + secondPOSTData2

    headerss["sequence-number"] = str(sequenceNumberHeader)
    secondPOSTResponse = requests.post("https://rtproxy-row.waze.com/rtserver/distrib/static", data=secondPOSTData, headers=headerss, cookies=cookieJar)

    cookieJar.update(secondPOSTResponse.cookies)
    sequenceNumberHeader += 1

    secondPOSTResponseData = secondPOSTResponse.content.hex()
    secondPOSTResponseData = decodeHexProtoBUF(secondPOSTResponseData)

    anonUserUsername = secondPOSTResponseData["1001"][1]["2220"]["1"]
    anonUserPassword = secondPOSTResponseData["1001"][1]["2220"]["2"]

    epochTime = int(time.time())

    mainPOSTData["1001"]["2184"]["28"] = epochTime

    thirdPOSTData2["1001"]["2744"]["1"]["1"] = anonUserUsername
    thirdPOSTData2["1001"]["2744"]["1"]["2"] = anonUserPassword

    thirdPOSTData3["1001"]["2108"]["1"] = UUID3

    thirdPOSTData1 = encodeToProtoBase64(mainPOSTData, mainPOSTTypeDef)
    thirdPOSTData2 = encodeToProtoBase64(thirdPOSTData2, thirdPOSTTypeDef2)
    thirdPOSTData3 = encodeToProtoBase64(thirdPOSTData3, thirdPOSTTypeDef3)

    thirdPOSTData = thirdPOSTData1 + "\n" + thirdPOSTData2 + "\n" + thirdPOSTData3

    headerss["sequence-number"] = str(sequenceNumberHeader)

    thirdPOSTResponseData = requests.post("https://rtproxy-row.waze.com/rtserver/distrib/login", headers=headerss, data=thirdPOSTData, cookies=cookieJar)

    cookieJar.update(thirdPOSTResponseData.cookies)
    sequenceNumberHeader += 1

    thirdPOSTResponseData = thirdPOSTResponseData.content.hex()
    thirdPOSTResponseData = decodeHexProtoBUF(thirdPOSTResponseData)

    authTokenMain = thirdPOSTResponseData["1001"][1]["2745"]["1"]["3"]
    globalServer = thirdPOSTResponseData["1001"][1]["2745"]["1"]["2"]
    userID = int(thirdPOSTResponseData["1001"][1]["2745"]["1"]["1"])

    binaryUserID = str(bin(userID)[2:])

    userIDBytes = []
    userIDBytes.append(b'12')

    while len(binaryUserID) < 31:
        binaryUserID = "0" + binaryUserID

    first = binaryUserID[:3]
    first = str(hex(int(first, 2))[2:])
    userIDBytes.append(bytes('0' + first, 'raw_unicode_escape'))

    binaryUserID = binaryUserID[3:]

    for i in range(1, 5):
        work = binaryUserID[:7]
        result = hex(int("1"+work, 2))[2:]

        userIDBytes.append(bytes(result, 'raw_unicode_escape'))
        binaryUserID = binaryUserID[7:]

    userIDBytes.append(b'08')
    userIDBytes = list(reversed(userIDBytes))

    rawUserIDBytes = ""
    for b in userIDBytes:
        b = chr(int(b, 16))
        rawUserIDBytes += b

    rawUserIDBytes = bytes(rawUserIDBytes, 'raw_unicode_escape')

    authTokenLen = len(authTokenMain)
    authTokenLenHex = hex(authTokenLen)[2:]
    authTokenLenHex = bytes([int(authTokenLenHex[i:i + 2],16) for i in range(0, len(authTokenLenHex), 2)])

    authTokenBuild = str(rawUserIDBytes.decode("raw_unicode_escape")) + str(authTokenLenHex.decode())
    authTokenBuild = authTokenBuild + authTokenMain

    finalUID = base64.b64encode(authTokenBuild.encode("raw_unicode_escape"))

    UID = finalUID

    headerss = {"uid": UID, "user-agent": "4.106.0.1", "sequence-number": str(sequenceNumberHeader), "x-waze-network-version": "3", "x-waze-wait-timeout": "3500"}

    return (headerss, globalServer, cookieJar)


# ============================================================================
# Upload Functions
# ============================================================================

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

voice_data_template = {
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
    """Create a JSON metadata file for the voice pack."""
    try:
        with open(file_path, "w") as meta_file:
            json.dump(data, meta_file)
    except IOError as e:
        print(f"Error creating metadata file: {e}")
        raise


def compress_files(source_dir, archive_name):
    """Compress files from source directory into a tar.gz archive."""
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
    """Encode voice data to Protocol Buffer and Base64."""
    try:
        encoded_data = blackboxprotobuf.encode_message(data, proto_buf_type_def)
        base64_encoded = base64.b64encode(encoded_data).decode("utf-8")
        return "ProtoBase64," + base64_encoded
    except Exception as e:
        print(f"Error encoding voice data: {e}")
        raise


def upload_data(url, headers, data, cookies):
    """Upload data to the specified URL."""
    try:
        response = requests.post(url, headers=headers, data=data, cookies=cookies)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Upload failed: {e}")
        raise


def upload(name_of_pack):
    """Upload a voice pack to Waze."""
    try:
        login_info = returnLoginHeader()
        headers = login_info[0]
        global_server = login_info[1]
        cookie_jar = login_info[2]
    except Exception as e:
        print(f"Error retrieving login information: {e}")
        return
    
    pack_uuid = str(uuid.uuid4())
    
    # Create a copy of the template for this upload
    voice_data = {
        '1001': {
            '2343': {
                '2': {
                    '1': bytes(pack_uuid, "UTF-8"),
                    '2': name_of_pack.replace("_FORMATTED", ""),
                    '5': global_server,
                    '12': 0
                },
                '3': b'TARGZMP3s'
            }
        }
    }
    
    metadata = {
        "uuid": pack_uuid,
        "set_name": name_of_pack,
        "owner": global_server,
        "revision": 0,
        "is_uploaded": 2,
        "has_new_version": 0
    }

    dir = rf"./mp3_upload/compressed_packs/{name_of_pack}/"
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
        print(f"✅ Upload of {name_of_pack} successful.")
    except Exception as e:
        print(f"❌ Upload of {name_of_pack} failed: {e}")
        return

    print(f"https://waze.com/ul?acvp={pack_uuid}")
    print(f"https://voice-prompts-ipv6.waze.com/{pack_uuid}.tar.gz\n")


def main():
    """Main function to upload all voice packs."""
    for folder in os.listdir(r"./mp3_upload/compressed_packs/"):
        upload(folder)


if __name__ == "__main__":
    main()
