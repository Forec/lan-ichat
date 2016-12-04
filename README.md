# LAN iChat （局域网内的视频聊天软件）

[![License](http://7xktmz.com1.z0.glb.clouddn.com/license-UDL.svg)](https://github.com/Forec/lan-ichat/blob/master/LICENSE) 
[![Build Status](https://travis-ci.org/Forec/lan-ichat.png)](https://travis-ci.org/Forec/lan-ichat) 
[![Doc](http://7xktmz.com1.z0.glb.clouddn.com/docs-icon.svg)](https://github.com/Forec/lan-ichat/)

> This project is a simple video chat tool.   
It supports IPv4 and IPv6, using TCP protocal temporarily. Not finished yet , next step is to change into UDP. **The current stable version is `v0.2`**, the current developing version is `v0.4`. **If you have thoughts for any of them, please [e-mail me](mailto:forec@bupt.edu.cn) or just open your PR, I am very glad to learn from your brilliant idea.**

**注：授权实验楼发表的教程对应版本为 v0.2， 该部分代码在 v0.2/Linux 下。**

## New Features
`v0.4` will provide the following abilities.
* Two hosts using different IP protocals can contact by a server, which has been  provided in `v0.3`. However, `v0.4` will reconstruct the classes (both server and client), the new version will use less bandwidth and memory.
* Everywhere, not only lan, can have an ichat using the server provided in `v0.4`. The `server` will be reconstructed using `Golang 1.7.3` in `v0.4`, which can improve a lot in performance.
* One of the typical using: Your host is in a college lan, using IPv6; another host is in the wide Internet, like home or hotel, using IPv4. The two hosts can build a contact.

## Platform (v0.2)

### Windows
The script is written in python 3.5, using some packages, all listed below.
* **cv2** : cv2 is the openCV packages for python. You can download `openCV` from its [official site](http://opencv.org/). Also, install by pip `pip install opencv-python` is needed. Then, install `ffmpeg`. Download it from [here](http://ffmpeg.org/), I suggest you chose the binary file and just install it simply. After you install `cv2`, `numpy` and `matplotlib` will also be installed.
* **pyaudio** : packages for dealing with audio. You can install it by `pip3 install pyaudio`.
* Built-in packages: `sys`, `struct`, `pickle`, `time`, `threading`, `argparse`, `zlib`, and `socket`.

### Linux
* To install `OpenCV` with Python support in Linux is a little troublesome. You can download [opencv.sh](http://7xktmz.com1.z0.glb.clouddn.com/opencv.sh) to install it easily, or follow these steps.
```bash
$ mkdir ichat && cd ichat
$ sudo apt-get install build-essential libgtk2.0-dev libjpeg-dev libtiff5-dev libjasper-dev libopenexr-dev cmake python-dev python-numpy python-tk libtbb-dev libeigen2-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev
$ wget https://github.com/Itseez/opencv/archive/2.4.13.zip
$ unzip 2.4.13.zip
$ cd 2.4.13
$ mkdir release && cd release
$ cmake -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_GTK=ON -D WITH_OPENGL=ON ..
$ sudo make
$ sudo make install
$ sudo nano /etc/ld.so.conf.d/opencv.conf   
$ Input /usr/local/lib and save
$ sudo ldconfig -v
$ sudo nano /etc/bash.bashrc
$ --Add the following two lines in the end of bash.bashrc
$ PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
  export PKG_CONFIG_PATH
```

* Attention, if you use Python3, you may need to specify the path. Add some options below.
```bash
$ cmake -D CMAKE_BUILD_TYPE=Release \
        -D CMAKE_INSTALL_PREFIX=/usr/local  \
           PYTHON3_EXECUTABLE=/usr/bin/python3 \
           PYTHON_INCLUDE_DIR=/usr/include/python3.4 \
           PYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.4m.so \
           PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.4/dist-packages/numpy/core/include ..
```

### Usage
Run `python3 main.py <parameters>`. Also, you can download the executable binary file `ichat.exe` from my cloud storage: [here](http://7xktmz.com1.z0.glb.clouddn.com/ichat.exe). Press `Esc` or `Ctrl-C` to stop this tool. The parameters are:
* --host: the remote host address you want to connect. Support IPv4 and IPv6. Default is `127.0.0.1`.
* --port: the port you want to use. The remote should use the same port as yours. Default is 10087. The tool use 2 ports, and if you set port to be `x`, another port will be `x+1`.
* --version or -v: the IP version you want to use. Default is 4, if you want to use IPv6, remember setting `--version=6`.
* --level: the image level you want. It could be 0, 1, 2, 3. Values bigger than 3 is same to 3. Level 0 is the best quality, that means you will see the original image of the remote camera. However, it requires high network condition. Default is 1. If your network is blocked, please use level 2 or 3.
* --noself: The tool will display both the remote and your videos in default. If you do not need to show yourself on your screen, use `--noself=True`. Do not set any value to this flag if you need to observe your image.
* In `Remote`, press `Esc` to quit, in `You`, press `Esc` to close the window of yourself, but chat remains.
* One screenshot for usage is below. I had an ichat with myself. If you double click `ichat.exe`, you will see yourself.    
<img src="http://7xktmz.com1.z0.glb.clouddn.com/ichat-show-1.png" width = "400px">

## Platform (v0.3)
### Server
* `v0.3` provides a file `server.py`, which is used to transmit data between IPv4 and IPv6. There are 4 instances created in running, the parameters are in format below. The first two parameters are the two ports used to receive connections from clients, and the next two parameters points the protocal they use. The last parameter shows the direction, `True` means client2 receives data from client1, `False` reverse it.
```python
    contact1to2v = Remote_Server(start_port, start_port+5, 6, 4, True)
    contact2to1v = Remote_Server(start_port+1, start_port+4, 6, 4, False)
    contact1to2a = Remote_Server(start_port+2, start_port+7, 6, 4, True)
    contact2to1a = Remote_Server(start_port+3, start_port+6, 6, 4, False)
```
* Above is an example: Assume the `start_port` is 10000, then the server will listen 8 ports (`10000` to `10007`), the first 4 ports will connect with remote client A's audio server/client and video server/client, and the next 4 ports will connect with another remote client B.
* According to the configuration, client A is using IPv6, client B is using IPv4.  
* As you can see, too much ports are used, so in the next version `v0.4`, I will reconstruct the models and use less ports. The current performance is not good, since many parameters are not adjusted. The next version `v0.4` will fix most of the problems.

### Client
* The data between client are all transmitted through server now. So in version `v0.3`, even two clients are in different LAN, they can still contact. However, the quality depends on the bandwidth of server. I want to find a way to let server make the two clients connect directly, however I have no idea until now.

### Usage
In server, run `python2 server.py` to start server, remember to check the 4 instances. In client, run `python3 main.py [OPTIONS]` to start client. Press `Esc` to stop the client. The new version can assign the following options. 
* --host: the remote server address. Support IPv4 and IPv6. Default is `127.0.0.1`.
* --port: the server port, which is the `start_port` in server code.
* --version: the IP version you want to use. Default is 4, if you want to use IPv6, remember setting `--version=6`.
* --level: the image level you want. It could be 0, 1, 2, 3. Values bigger than 3 is same to 3. Level 0 is the best quality, that means you will see the original image of the remote camera. However, it requires high network condition. Default is 1. If your network is blocked, please use level 2 or 3.
* --noself: The tool will display both the remote and your videos in default. If you do not need to show yourself on your screen, use `--noself=True`. Do not set any value to this flag if you need to observe your image.

## Update-logs
* 2016-9-23: Add this project, video is ok. Define `v0.1`.
* 2016-9-24: Add audio transmission, add quality settings, defile `v0.2`.
* 2016-10-6: Build repository.
* 2016-10-9: Add Linux version for `v0.2`.
* 2016-10-13: Add authorisation.
* 2016-11-1: Start updating to `v0.3`, supply a protocal-crossed version, two hosts using IPv4 and IPv6 can contact in this version.
* 2016-11-2: Finish `v0.3`, which is an unstable version, it will be improved a lot in `v0.4`.
* 2016-12-4: Build test, ready to update v0.4 before 2017.

# License
All codes in this repository are licensed under the terms you may find in the file named "LICENSE" in this directory.

# 授权声明
我已授权[实验楼](https://www.shiyanlou.com/)使用此仓库中的代码并发表此项目教程，你可以在这里查看对应的[教程](https://www.shiyanlou.com/courses/672)。