import os
import shlex
import time
import uuid
from subprocess import Popen
from flask import Flask, request, render_template, session, redirect

from phonopi.services.butt import ButtService, MockButtService


class PhonoWebApp:

    def __init__(self, run_services=True):
        # Setup flask app
        self.app = Flask(__name__)
        self.app.route('/')(self.home)
        self.app.route('/butt/streaming')(self.streaming)
        self.app.route('/butt/recording', methods=['POST', 'GET'])(self.toggle_recording)
        self.app.route('/butt/manage_recordings')(self.manage_recordings)
        self.app.route('/butt/manage_recordings/rename', methods=['POST'])(self.manage_recordings_rename)
        self.app.route('/butt/manage_recordings/del', methods=['POST'])(self.manage_recordings_del)
        self.app.route('/vlc')(self.manage_vlc)
        self.app.route('/piadmin/reboot')(self.admin_reboot)
        self.app.route('/piadmin/shutdown')(self.admin_shutdown)
        self.app.secret_key = str(uuid.uuid4())

        # Setup services
        if run_services:
            self.butt = ButtService()
            self.butt.start_butt()

            self.vlc_process = Popen(shlex.split("cvlc --http-port 7777 --http-password 1238"))

        else:
            self.butt = MockButtService()
            self.vlc_process = None

    def home(self):
        butt = self.butt.status
        if self.vlc_process is None:
            vlc = False
        else:
            vlc = self.vlc_process.poll() is None
        return render_template('index.html', butt=butt, vlc=vlc)

    def streaming(self):
        return str(self.butt.status.connected)

    def toggle_recording(self):
        if request.method == 'POST':
            if self.butt.status.recording:
                self.butt.stop_recording()
            else:
                self.butt.start_recording()

        return str(self.butt.status.recording)

    def manage_recordings(self):
        msg = session.pop('msg', None)
        return render_template('manage_recordings.html', recordings=self.butt.list_recordings(), msg=msg)

    def manage_recordings_rename(self):
        self.butt.rename_recording(request.form.get('fn'), request.form.get('new_name'))
        session['msg'] = "Recording renamed and moved to music library."
        return redirect('/butt/manage_recordings')

    def manage_recordings_del(self):
        self.butt.delete_recording(request.form.get('fn'))
        session['msg'] = "Recording deleted successfully"
        return redirect('/butt/manage_recordings')

    def manage_vlc(self):
        return render_template('manage_vlc.html')

    def admin_reboot(self):
        os.popen(f'sudo reboot now')

    def admin_shutdown(self):
        os.popen(f'sudo shutdown now')



if __name__ == '__main__':
    PhonoWebApp().app.run(host='0.0.0.0', port=80)