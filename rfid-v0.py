#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import time
import datetime
import urllib.request
import logging
#import base64
import binascii
import sys

# A UDP server

# Set up a UDP server
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Listen on port 21567
# (to all IP addresses on this system)
listen_addr = ("",8080)
UDPSock.bind(listen_addr)

urlHeadString = "http://data.sunplusit.com/Api/DoorRFIDInfo?code=83E4621643F7B2E148257244000655E3&rfid="
stringTAGforSunplusIT = "3000e200"
tagLength = 28  # the length for web server
debugPrint = False
#periodTimeDouble = 30  #幾秒內重複刷到的予以忽略


lastTailTime = 0

def is_json(myjson):
    try:
        json_object = json.loads(myjson)

    except ValueError:
        return False

    return True

def chkDouble(chkData, dataList, timeList=[]):
    rtnValue = False
    #print("Check {} records in DB".format(len(dataList)))

    for i in range(len(dataList)):
        if(chkData==dataList[i]):
            nowTime = time.time()
            #print("     check DB: {}, Time diff: {}".format(dataList[i], nowTime-timeList[i]))
            #if(nowTime-timeList[i]<periodTimeDouble):  #如果還在忽略秒數之內
            rtnValue = True
            break

    #print("     --> Check: {} , decide: {}".format(chkData, rtnValue))

    return rtnValue

def punchTAG(TAG):
    print("Punch: {}".format(TAG))

def scanTAGS(readHEX):
    global stringTAGforSunplusIT, tagLength
    tagsFound = {}
    tagsTime = {}

    posHead = readHEX.find(stringTAGforSunplusIT)
    if(posHead>=0):
        #print("Received RFID: {}".format(readHEX))

        i = 0
        while posHead>0:
            #print("RFID: {}".format(readHEX))
            posHead = readHEX.find(stringTAGforSunplusIT)
            tmpValue = readHEX[posHead:posHead+28]
            if(posHead>=0 and chkDouble(tmpValue, tagsFound, tagsTime) == False and len(tmpValue)==tagLength):
                tagsFound[i] = tmpValue
                tagsTime[i] = time.time()
                #print("Found new tag #{}: {} --> time:{}".format(i, tagsFound[i], tagsTime[i]))
                readHEX = readHEX[posHead+28:]
                #將此TAG打卡
                #punchTAG(tagsFound[i])
                i += 1

            else:
                readHEX = readHEX[posHead+1:]

        #print("Found TAGS ----> {}".format(len(tagsFound)))
        return (tagsFound, tagsTime)

    else:
        return ([],[])

#目前掃到的TAGS
tmpTAGS = {}
tmpTIMES = {}  #目前掃到的TIME

while True:
    data,addr = UDPSock.recvfrom(1024)
    tmpTAGS, tmpTIMES = scanTAGS(binascii.b2a_hex(data).decode('ascii'))
    print("Found TAGS: {}, TIMES: {}".format(len(tmpTAGS), len(tmpTIMES)))
    for i in range(0,len(tmpTAGS)):
        print ("TAG: {}, Time: {}".format(tmpTAGS[i], tmpTIMES[i]))

    print("-------------------------------")

'''
        try:
            webReply = urllib.request.urlopen(urlHeadString + readHEX).read()
            webReply = webReply.decode('utf-8').rstrip()
            #logger.info('webReply: {}'.format(webReply))
            if(debugPrint==True):
                print(urlHeadString + readHEX)
                print("webReply:" + webReply)

        listTAGs = webReply.split("")

        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            logger.info('Unexpected error:' + str(sys.exc_info()[0]))
            webReply = "[]"
            pass
           
        if(is_json(webReply)==True):
            jsonReply = json.loads(webReply)
            print (jsonReply)
'''
