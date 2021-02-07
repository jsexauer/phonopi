# phonopi
Raspberry PI project to integrate record player, Spotify, and MP3 collection into stereo system

## TODO
- web page to show status of Butt, IceCast, etc..
- start/stop recordings from record
- see if nice app in iOS
- setup music
- backup image
  - https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=247568
  - https://www.raspberrypi.org/documentation/linux/filesystem/backup.md
  - https://www.tomshardware.com/how-to/back-up-raspberry-pi-as-disk-image


## Install Steps

### IceCast2
Install icecast: https://icecast.org/docs/
Hosted on port 8000
```
sudo apt-get instal icecast2
```

### Butt
Install butt from source: 
https://danielnoethen.de/butt/manual.html#_install

```
sudo apt-get install libfltk1.3-dev portaudio19-dev libopus-dev libmp3lame-dev libvorbis-dev libogg-dev libflac-dev libdbus-1-dev libsamplerate0-dev libssl-dev
```

Note AAC not supported, so removed that package from install. Also do ./configure --disable-aac

```
tar -xzf butt-<version>.tar.gz
cd butt-<version>
./configure --disable-aac
make
sudo make install
```

Installed to: \usr\local\bin\butt

### Spotify Connect with Raspotify
https://github.com/dtcooper/raspotify

```
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
```

Edit /etc/default/raspotify to give a cool name and icon, etc..
sudo service raspotify restart

### VLC
```
cvlc --http-port 7777 --http-password 1238 
```

https://wiki.videolan.org/Documentation:Modules/http_intf/#VLC_2.0.0_and_later

### Samba
https://www.raspberrypi.org/forums/viewtopic.php?t=214546

### Run at startup
Edit /etc/rc.local

```
sudo sh -c 'cd /home/pi/projects/phonopi && python3 -m phonopi &'
```

Headless startup:
https://stackoverflow.com/questions/9699992/how-to-start-linux-with-gui-without-monitor