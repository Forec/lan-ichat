# last edit date: 2016/09/24
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
import pyaudio
import wave
import sys
import zlib
import struct
import pickle
import time
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.5

class Audio_Server(threading.Thread):
    def __init__(self, port, version) :
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = ('', port)
        if version == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)
        self.p = pyaudio.PyAudio()
        self.stream = None
    def __del__(self):
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
    def run(self):
        print("AUDIO server starts...")
        self.sock.bind(self.ADDR)
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        print("remote AUDIO client success connected...")
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer = CHUNK
                                  )
        while True:
            while len(data) < payload_size:
                data += conn.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]
            while len(data) < msg_size:
                data += conn.recv(81920)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frames = pickle.loads(frame_data)
            for frame in frames:
                self.stream.write(frame, CHUNK)

class Audio_Client(threading.Thread):
    def __init__(self ,ip, port, version):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.p = pyaudio.PyAudio()
        self.stream = None
        print("AUDIO client starts...")
    def __del__(self) :
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
    def run(self):
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print("AUDIO client connected...")
        self.stream = self.p.open(format=FORMAT, 
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        while self.stream.is_active():
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = self.stream.read(CHUNK)
                frames.append(data)
            senddata = pickle.dumps(frames)
            try:
                self.sock.sendall(struct.pack("L", len(senddata)) + senddata)
            except:
                break