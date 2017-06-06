from App import App
from DockerShell import DockerShell


class Kernel:
    def __init__(self):
        self.__dockerShell = DockerShell()

        app = App(self.__dockerShell).run()
