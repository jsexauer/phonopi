import shlex
from subprocess import Popen
from flask import Flask, request

from phonopi.services.butt import ButtService


class PhonoWebApp:

    def __init__(self):
        # Setup flask app
        self.app = Flask(__name__)
        self.app.route('/')(self.home)
        self.app.route('/butt/toggle_recording')(self.toggle_recording)
        self.app.route('/butt/manage_recordings')(self.manage_recordings)
        self.app.route('/butt/manage_recordings/rename', methods=['POST'])(self.manage_recordings_rename)
        self.app.route('/butt/manage_recordings/del', methods=['POST'])(self.manage_recordings_del)

        # Setup services
        self.butt = ButtService()
        self.butt.start_butt()

        self.vlc_process = Popen(shlex.split("cvlc --http-port 7777 --http-password 1238"))

    def home(self):
        butt = self.butt.status
        return f"""
        <h1>PhonoPi</h1>
        <h3>Vinyl</h3>
        <ul>
            <li><a href="http://phonopi:8000/phono">Listen to vinyl!</a></li>
            <li><a href="/butt/toggle_recording">
                {'Stop ' if butt.recording else 'Start '} recording vinyl to mp3
            </a></li>
            <li><a href="/butt/manage_recordings">
                Manage Recordings
            </a></li>
        </ul>
        <h3>MP3</h3>
        <ul>
            <li><a href="http://phonopi:7777">MP3 Control</a> -- password: 1238  (no username)</li>
        </ul>
        
        
        <h2>Status</h2>
        <h3>Butt</h3>
        Alive: {butt.alive} <br/>
        Streaming: {butt.connected} <br/>
        Recording: {butt.recording} <br/>
        """

    def toggle_recording(self):
        if self.butt.status.recording:
            self.butt.stop_recording()
            return "Stopped recording..."
        else:
            self.butt.start_recording()
            return "Started recording..."

    def manage_recordings(self):
        result = "<table border=0>"
        result += "<tr><th>Recording</th><th>Rename</th><th>Delete</th></tr>"
        for fn in self.butt.list_recordings():
            result += f"""<tr>
                <td>{fn}</td>
                <td><form action="/butt/manage_recordings/rename" method="POST">
                <input type="hidden" value="{fn}" name="fn" ></input>
                    <input type="text" name="new_name" ></input>
                    <input type="submit" ></input>
                </form></td>
                <td><form action="/butt/manage_recordings/del" method="POST">
                    <input type="hidden" value="{fn}" name="fn" ></input>
                    <input type="submit" value="Delete" ></input>
                </form></td>
            </tr>"""
        return result

    def manage_recordings_rename(self):
        self.butt.rename_recording(request.form.get('fn'), request.form.get('new_name'))
        return "Rename successful"

    def manage_recordings_del(self):
        self.butt.delete_recording(request.form.get('fn'))
        return "Recording deleted"



if __name__ == '__main__':
    PhonoWebApp().app.run(host='0.0.0.0', port=80)