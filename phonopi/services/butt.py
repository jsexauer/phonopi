"""
Interact with BUTT (Broadcast Using This Tool)

This is the tool that sends the phonograph input to IceCast so that you can stream it as an
internet radio station.
"""
import os
from pathlib import Path

class ButtStatus:
    def __init__(self, raw_status):
        self.alive = False
        self.connected = False
        self.connecting = False
        self.recording = False

        if "No butt instance" in raw_status:
            return # Service has not been started

        self.alive = True

        # Sample:
        # connected: 1
        # connecting: 0
        # recording: 0
        lines = [l.split(": ") for l in raw_status.split("\n")]

        self.connected = lines[0][1] == '1'
        self.connecting = lines[1][1] == '1'
        self.recording = lines[2][1] == '1'




class ButtService(object):
    """
    Wrapper around command line control of butt
    https://danielnoethen.de/butt/manual.html#_command_line_control
    """

    def __init__(self):
        self.port = 7701
        self.recordings_path = Path('/home/pi/phono_recordings')


    def start_butt(self):
        self._call('&') # start as a background task

    @property
    def status(self):
        return ButtStatus(self._call('-S'))

    def connect(self):
        """Connect and start streaming"""
        if self.status or self.status:
            return # Don't try to connect multiple times

        self._call('-s')

    def disconnect(self):
        if not self.status.connected:
            return # Don't try to disconnect when already disconnected

        self._call('-d')

    def start_recording(self):
        if self.status.recording:
            return # Don't try recording when allready recording
        self._call('-r')

    def stop_recording(self):
        if not self.status.recording:
            return
        self._call('-t')

    def _call(self, command):
        return os.popen(f'butt -p {self.port} ' + command).read()

    def list_recordings(self):
        for f in self.recordings_path.glob("*.mp3"):
            yield f.name

