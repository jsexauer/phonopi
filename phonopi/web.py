import shlex
import time
from subprocess import Popen
from flask import Flask, request, render_template

from phonopi.services.butt import ButtService


class PhonoWebApp:

    def __init__(self, run_services=True):
        # Setup flask app
        self.app = Flask(__name__)
        self.app.route('/')(self.home)
        self.app.route('/butt/recording', methods=['POST', 'GET'])(self.toggle_recording)
        self.app.route('/butt/manage_recordings')(self.manage_recordings)
        self.app.route('/butt/manage_recordings/rename', methods=['POST'])(self.manage_recordings_rename)
        self.app.route('/butt/manage_recordings/del', methods=['POST'])(self.manage_recordings_del)

        # Setup services
        self.butt = ButtService(mock=not run_services)

        if run_services:
            self.butt.start_butt()

            self.vlc_process = Popen(shlex.split("cvlc --http-port 7777 --http-password 1238"))

    def home(self):
        butt = self.butt.status
        return render_template('index.html', butt=butt)

    def toggle_recording(self):
        if request.method == 'POST':
            if self.butt.status.recording:
                self.butt.stop_recording()
            else:
                self.butt.start_recording()
            # Wait for butt to take action
            time.sleep(0.5)

        return str(self.butt.status.recording)

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