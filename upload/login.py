import sys
import blackboxprotobuf
import base64
import uuid
import json
import time
import requests

def decodeHexProtoBUF(hexString):
    message, bufType = blackboxprotobuf.protobuf_to_json(base64.b16decode(hexString, True))
    return json.loads(message)

def encodeToProtoBase64(jsonData, protoType):
    return 'ProtoBase64,' + str(base64.b64encode(blackboxprotobuf.encode_message(jsonData, protoType)), 'utf-8')

def returnLoginHeader():
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