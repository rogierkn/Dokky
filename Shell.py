import subprocess
from threading import Thread

import _thread

class Shell:

    @staticmethod
    def run(command, threaded=False):
        if not threaded:
            return subprocess.getoutput([command])
        else:
            thread = Thread(target=Shell.threadedRun, args=(command,))
            thread.start()


    @staticmethod
    def threadedRun(command):
        subprocess.getoutput([command])
