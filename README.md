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
sudo apt-get install icecast2
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

1. Start butt
1. Settings.  Add server (phonopi at 8000, using stream password.  phono mountpoint)
1. Add a stream info.  Be sure to check make it public checkbox.
1. Audio tab, choose C-Media sound card.  Streaming via OGG/VORBIS.  192k bitrate.  Recording Mp3 (default).  Signal present/absent at -48 dB
1. Streaming tab, start if signal present for 1 second, stop if absent for 15 seconds.
1. Record tab, change record directory to: /home/pi/phono_recordings
1. Back on Main tab, save.

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

vncserver :42
export DISPLAY=:42
butt -p 7701