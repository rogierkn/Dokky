import subprocess

class Shell:

    @staticmethod
    def run(command):
        return subprocess.getoutput([command])
