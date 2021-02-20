# phonopi
Raspberry PI project to integrate record player, Spotify, and MP3 collection into stereo system


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
1. Settings.  Add server (phonopi at 8000, using stream password.  phono.mp3 mountpoint -- must have .mp3 at the end)
1. Add a stream info.  Be sure to check make it public checkbox.
1. Audio tab, Streaming via MP3.  192k bitrate.  Recording Mp3 (default).  Signal present/absent at -28 dB
1. Streaming tab, start if signal present for 1 second, stop if absent for 15 seconds.
1. Record tab, change record directory to: /home/pi/phono_recordings
1. Back on Main tab, save.

In order to run it headless, use xvfb:
```
sudo apt-get install xvfb
xvfb-run -a butt
```

### Spotify Connect with Raspotify
https://github.com/dtcooper/raspotify

```
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
```

Edit /etc/default/raspotify to give a cool name and icon, etc..

Edit /usr/share/alsa/alsa.conf

Replace
```
defaults.ctl.card 0
defaults.pcm.card 0
```
with
```
defaults.ctl.card 1
defaults.pcm.card 1
```

sudo service raspotify restart

### VLC
1. Open VLC.
1. Set library and playlist.
1. Tools > Preferences > All radio button > Interface > Main Interfaces.  Enable Web.
```
cvlc --http-port 7777 --http-password 1238 
```

https://wiki.videolan.org/Documentation:Modules/http_intf/#VLC_2.0.0_and_later

### Samba
https://www.raspberrypi.org/forums/viewtopic.php?t=214546
https://docs.huihoo.com/ubuntu/9.04/internet/C/networking-shares.html
```
sudo apt install samba samba-common-bin smbclient cifs-utils
sudo nano /etc/samba/smb.conf
```
At bottom:
```
[music]
    path = /home/pi/Music
    read only = no
    public = yes
    writable = yes
    browseable = yes
    guest ok = yes
```
Add a password for smb:
```
sudo smbpasswd -a pi
```

### Pi Hole
https://pi-hole.net/

```
curl -sSL https://install.pi-hole.net | bash
sudo nano /etc/lighttpd.conf
# Edit serve.port to use 81
```

Configure it to be the DHCP server of the network.

Goto http://10.205.1.1/ui/1.0.99.202617/dynamic/home.html and turn off DHCP server.


### Run at startup
Install authbind to allow running on port 80 as normal user
```
sudo apt-get install authbind
sudo touch /etc/authbind/byport/80
sudo chmod 777 /etc/authbind/byport/80
```

Edit /etc/rc.local placing this line above exit 0 (the ampersand is important)

```
runuser -l pi -c 'authbind --deep python3 /home/pi/projects/phonopi/run_phonopi.py &'
```

To kill at after startup:
```
ps aux | grep python3
kill <pid>
ps aux | grep butt
kill <pid>
```
