from enum import Enum

import rumps
import json

import time

import subprocess

import Util
from DockerShell import DockerShell


class Container:
    def __init__(self, id: str, dockerShell):
        self.__id = id
        self.__dockerShell = dockerShell
        self.updateData()
        self.__createMenuItem()

    def update(self):
        self.updateData()
        self.updateMenuItem()

    def updateData(self):
        self.__data = json.loads(self.__dockerShell.getContainerInfo(self.__id))[0]

    def updateMenuItem(self):
        self.__menuItem.title = self.__data["Name"] + " - " + self.__data["Config"]["Hostname"]
        self.__menuItem.icon = self.getStatusIcon()

    def __createMenuItem(self):
        self.__menuItem = rumps.MenuItem(
                title=self.__id,
                callback=self.__click,
                key=self.__id,
                dimensions=(15, 15)
        )

    def __click(self, sender):
        print("Clicked on " + self.__id)
        # print(self.__dockerShell.getContainerInfo(self.__id))
        Util.to_clipboard(self.__id)
        if self.getStatus() == Status.On:
            self.__dockerShell.stopContainer(self.__id)
        else:
            self.__dockerShell.startContainer(self.__id)


    def getMenuItem(self) -> rumps.MenuItem:
        return self.__menuItem


    def getId(self):
        return self.__id


    def getStatus(self):
        status = Status.Off
        statusData = self.__data["State"]
        if statusData["Status"] == "running":
            status = Status.On

        return status


    def getStatusIcon(self):
        if self.getStatus() == Status.Off:
            return './assets/status_off.png'
        elif self.getStatus() == Status.On:
            return './assets/status_on.png'
        else:
            return './assets/icon.png'


# used to have consistent statuses of containers
class Status(Enum):
    Off = 0
    On = 1
    Paused = 2
    Restarting = 3
