# last edit date: 2016/11/2
# author: Forec
# LICENSE
# Copyright (c) 2015-2017, Forec <forec@bupt.edu.cn>

# Permission to use, copy, modify, and/or distribute this code for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from socket import *
import threading
import cv2
import sys
import struct
import pickle
import time
import zlib
import numpy as np

class Video_Server(threading.Thread):
    def __init__(self, remoteIP, remotePort, remoteVersion) :
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (remoteIP, remotePort)
        if remoteVersion == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)
    def __del__(self):
        if self.sock is not None:
            self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass
    def run(self):
        print ("VEDIO server starts...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print ("video server <-> remote server success connected...")
        check = "F"
        check = self.sock.recv(1)
        if check.decode("utf-8") != "S":
            return
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")
        cv2.namedWindow('Remote', cv2.WINDOW_NORMAL)
        while True:
            while len(data) < payload_size:
                data += self.sock.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]
            while len(data) < msg_size:
                data += self.sock.recv(81920)
            zframe_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(frame_data)
            try:
                cv2.imshow('Remote', frame)
            except:
                pass
            if cv2.waitKey(1) & 0xFF == 27:
                break

class Video_Client(threading.Thread):
    def __init__(self ,serverIP, serverPort, serverVersion, showme, level):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (serverIP, serverPort)
        self.showme = showme
        self.level = level
        if level == 0:
            self.interval = 0
        elif level == 1:
            self.interval = 1
        elif level == 2:
            self.interval = 2
        else:
            self.interval = 3
        self.fx = 1 / (self.interval + 1)
        if self.fx < 0.3:
            self.fx = 0.3
        if serverVersion == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.cap = None
    def __del__(self) :
        if self.sock is not None:
            self.sock.close()
        if self.cap is not None:
            self.cap.release()
        if self.showme:
            try:
                cv2.destroyAllWindows()
            except:
                pass
    def run(self):
        print ("VEDIO client starts...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print ("video client <-> remote server success connected...")
        check = "F"
        check = self.sock.recv(1)
        if check.decode("utf-8") != "S":
            return
        print ("receive authend")
        self.cap = cv2.VideoCapture(0)
        if self.showme:
            cv2.namedWindow('You', cv2.WINDOW_NORMAL)
        print ("remote VEDIO client connected...")
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if self.showme:
                cv2.imshow('You', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    self.showme = False
                    cv2.destroyWindow('You')
            if self.level > 0:
                frame = cv2.resize(frame, (0,0), fx=self.fx, fy=self.fx)
            data = pickle.dumps(frame)
            zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            try:
                self.sock.sendall(struct.pack("L", len(zdata)) + zdata)
                print("video send ", len(zdata))
            except:
                break
            for i in range(self.interval):
                self.cap.read()