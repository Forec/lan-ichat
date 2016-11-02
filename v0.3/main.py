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

import sys
import time
import argparse
from vchat import Video_Server, Video_Client
from achat import Audio_Server, Audio_Client

parser = argparse.ArgumentParser()

parser.add_argument('--shost', type=str, default='127.0.0.1')
parser.add_argument('--sport', type=int, default=10087)
parser.add_argument('--sversion', type=int, default=4)
# parser.add_argument('--rhost', type=str, default='127.0.0.1')
# parser.add_argument('--rport', type=int, default=10087)
# parser.add_argument('--rversion', type=int, default=4)
parser.add_argument('--noself', type=bool, default=False)
parser.add_argument('--level', type=int, default=1)

args = parser.parse_args()

sIP = args.shost
sPORT = args.sport
sVERSION = args.sversion
# rIP = args.rhost
# rPORT = args.rport
# rVERSION = args.rversion
SHOWME = not args.noself
LEVEL = args.level

if __name__ == '__main__':
    vclient = Video_Client(sIP, sPORT, sVERSION, SHOWME, LEVEL)
    vserver = Video_Server(sIP, sPORT+1, sVERSION)
    aclient = Audio_Client(sIP, sPORT+2, sVERSION)
    aserver = Audio_Server(sIP, sPORT+3, sVERSION)
    vclient.start()
    vserver.start()
    aclient.start()
    aserver.start()
    while True:
        time.sleep(1)
        if not vserver.isAlive() or not vclient.isAlive():
            print("Video connection lost...")
            sys.exit(0)
        if not aserver.isAlive() or not aclient.isAlive():
            print("Audio connection lost...")
            sys.exit(0)