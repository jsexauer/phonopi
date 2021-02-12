"""
Interact with BUTT (Broadcast Using This Tool)

This is the tool that sends the phonograph input to IceCast so that you can stream it as an
internet radio station.
"""
import os
import shlex
import shutil
import time
from pathlib import Path
from subprocess import Popen
from threading import Lock


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
        self._butt_cmd = 'butt'
        self._port = 7701
        self._butt_proc = None
        self.temp_recordings_path = Path('/home/pi/phono_recordings')
        self.permanent_recordings_path = Path('/home/pi/Music/vinyl')
        self._butt_cmd_lock = Lock()


    def start_butt(self):
        if self.status.alive:
            return # don't try to butt again

        # Run butt headlessly
        # https://askubuntu.com/questions/50599/how-do-you-run-a-gui-application-without-gui-gui-application-as-daemon-on-headl
        self._butt_proc = Popen(shlex.split(f"xvfb-run -a {self._butt_cmd} -p {self._port} -c /home/pi/.buttrc"))

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
            return # Don't try recording when already recording
        self._call('-r', hold_lock=1)

    def stop_recording(self):
        if not self.status.recording:
            return
        self._call('-t', hold_lock=1)

    def list_recordings(self):
        for f in self.temp_recordings_path.glob("*.mp3"):
            yield f.name

    def rename_recording(self, orig_fn: str, new_fn: str):
        """Rename recording and move to permanent home"""
        if not new_fn.lower().endswith('.mp3'):
            new_fn += ".mp3"

        shutil.move(self.temp_recordings_path / orig_fn, self.permanent_recordings_path / new_fn)

    def delete_recording(self, fn: str):
        (self.temp_recordings_path / fn).unlink()

    def _call(self, command, hold_lock=0):
        with self._butt_cmd_lock:
            result = os.popen(f'{self._butt_cmd} -p {self._port} ' + command).read()
            if hold_lock != 0:
                # Some commands take a moment to execute.  If another command comes while it's pending, it will be lost.
                time.sleep(hold_lock)
            return result


class MockButtService(ButtService):

    def __init__(self):
        super().__init__()
        self._status = ButtStatus("No butt instance")
        self._status.connected = True

        self._files = ['file1.mp3', 'file2.mp3', 'file3.mpr']

    @property
    def status(self):
        return self._status

    def list_recordings(self):
        return self._files

    def start_recording(self):
        self._status.recording = True

    def stop_recording(self):
        self._status.recording = False

    def rename_recording(self, orig_fn: str, new_fn: str):
        self._files.remove(orig_fn)

    def delete_recording(self, fn: str):
        self._files.remove(fn)

    def _call(self, command):
        raise NotImplemented("Not in Mock")