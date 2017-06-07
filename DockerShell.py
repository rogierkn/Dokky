import typing

from Shell import Shell


class DockerShell:
    def getContainerIds(self) -> typing.List[str]:
        containersString = Shell.run("docker ps -a -q")
        if (containersString == ''):
            return list()
        return containersString.split("\n")

    def getContainerInfo(self, id) -> str:
        return Shell.run("docker inspect " + id)

    def startContainer(self, id):
        return Shell.run("docker start " + id, True)

    def stopContainer(self, id):
        return Shell.run("docker stop " + id, True)