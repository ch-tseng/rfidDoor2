#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import urllib.request
import logging
import json
#import base64
import binascii
import sys
import time

# A UDP server

# Set up a UDP server
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Listen on port 21567
# (to all IP addresses on this system)
listen_addr = ("",8080)
UDPSock.bind(listen_addr)
debugPrint = False
urlLoadTagsDB = "http://data.sunplusit.com/Api/DoorRFIDInfo?code=83E4621643F7B2E148257244000655E3"
urlHeadString = "http://data.sunplusit.com/Api/DoorRFIDInfo?code=83E4621643F7B2E148257244000655E3&rfid="

#-----------------------------------------
#logging記錄
logger = logging.getLogger('msg')
hdlr = logging.FileHandler('/home/chtseng/rfidDoor/msg.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

tagDB = []

#-----------------------------------------
def loadDB():
    global tagDB

    try:
        print("Start load all tags into db...")
        logger.info("Start load all tags into db...")

        webReply = urllib.request.urlopen(urlLoadTagsDB).read()
        webReply = webReply.decode('utf-8').rstrip()
        logger.info('DB load: {}'.format(webReply))
        if(debugPrint==True):
            print('webReply: {}'.format(webReply))
            print(urlLoadTagsDB)
            print("webReply:" + webReply)

        if(is_json(webReply)==True):
            tagDB = json.loads(webReply)
            print("Total {} tags are loaded to DB.".format(len(tagDB)))
            logger.info("Total {} tags are loaded to DB.".format(len(tagDB)))

    except Exception:
        print("Unexpected error while load tags DB:", sys.exc_info()[0])
        logger.info('Unexpected error while load tags db:' + str(sys.exc_info()[0]))
        pass


def is_json(myjson):
    try:
        json_object = json.loads(myjson)

    except ValueError:
        return False

    return True

#loadDB()

while True:
    data,addr = UDPSock.recvfrom(1024)
    #tmpTAGS, tmpTIMES = scanTAGS(binascii.b2a_hex(data).decode('ascii'))
    readHEX = binascii.b2a_hex(data).decode('ascii')
    logger.info('Received rfid:' + readHEX)
    if(debugPrint==True):
        print (readHEX)

    try:
        webReply = urllib.request.urlopen(urlHeadString + readHEX).read()
        webReply = webReply.decode('utf-8').rstrip()
        logger.info('webReply: {}'.format(webReply))
        if(debugPrint==True):
            print('webReply: {}'.format(webReply))
            print(urlHeadString + readHEX)
            print("webReply:" + webReply)

       #     listTAGs = webReply.split("")

    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        logger.info('Unexpected error:' + str(sys.exc_info()[0]))
        webReply = "[]"
        pass

    if(is_json(webReply)==True):
        jsonReply = json.loads(webReply)
        if(debugPrint==True):
            print (jsonReply)

    #time.sleep(1)
