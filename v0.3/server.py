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
import sys
import time
import zlib

class Remote_Server(threading.Thread):
    def __init__(self, port1, port2, version1, version2, direc) :
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR1 = ('', port1)
        self.ADDR2 = ('', port2)
        self.dir = direc
        if version1 == 4:
            self.sock1 = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock1 = socket(AF_INET6 ,SOCK_STREAM)
        if version2 == 4:
            self.sock2 = socket(AF_INET ,SOCK_STREAM)
        else:
            self.sock2 = socket(AF_INET6 ,SOCK_STREAM)
        self.sock1.bind(self.ADDR1)
        self.sock2.bind(self.ADDR2)
    def __del__(self):
        if self.sock1 is not None:
            self.sock1.close()
        if self.sock2 is not None:
            self.sock2.close()
    def run(self):
        self.sock1.listen(1)
        conn1, _ = self.sock1.accept()
        print "remote client1 connected..."
        self.sock2.listen(1)
        conn2, _ = self.sock2.accept()
        print "remote client2 connected..."
        conn1.sendall("S")
        conn2.sendall("S")
        while True:
            if self.dir:
                data = conn1.recv(81920)
                conn2.sendall(data)
            else:
                data = conn2.recv(81920)
                conn1.sendall(data)

if __name__ == '__main__':
    start_port = 10131
    contact1to2v = Remote_Server(start_port, start_port+5, 6, 4, True)
    contact2to1v = Remote_Server(start_port+1, start_port+4, 6, 4, False)
    contact1to2a = Remote_Server(start_port+2, start_port+7, 6, 4, True)
    contact2to1a = Remote_Server(start_port+3, start_port+6, 6, 4, False)
    contact1to2v.start()
    contact2to1v.start()
    contact1to2a.start()
    contact2to1a.start()
    while True:
        time.sleep(1)