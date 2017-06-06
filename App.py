import rumps
from typing import Dict
from Container import Container


class App(rumps.App):
    def __init__(self, dockerShell):
        rumps.debug_mode(True)
        super().__init__("DockerMenu", icon="./assets/icon.png")

        self.__dockerShell = dockerShell

        self.__containers = dict()

        self.__menuUpdater = rumps.Timer(self.refresh, 10).start()
        self.__containerUpdate = rumps.Timer(self.updateContainers, 5).start()

    # Update the containers
    # Add newly created, remove the removed containers
    def refresh(self, sender):

        currentContainers = self.__containers.keys()
        dockerContainers = self.__dockerShell.getContainerIds()
        print("------\n")
        print("Currently have {0} containers".format(len(currentContainers)))
        print("Docker currently reports {0} containers".format(len(dockerContainers)))

        containersToCreate = list(filter(lambda id: id not in currentContainers, dockerContainers))
        containersToRemove = list(filter(lambda id: id not in dockerContainers, currentContainers))

        print("Found {0} new containers".format(len(containersToCreate)))
        print("Have to remove {0} containers".format(len(containersToRemove)))

        self.__removeContainers(containersToRemove)
        self.__addContainers(containersToCreate)

        self.__updateMenu()

    def __removeContainers(self, containersToRemove):
        for id in containersToRemove:
            self.__containers.pop(id)

    def __addContainers(self, containersToCreate):
        for id in containersToCreate:
            container = Container(id, self.__dockerShell)
            self.__containers[id] = container

    def __updateMenu(self):
        menuItems = list(map(lambda container: container.getMenuItem(), self.__containers.values()))
        menuItems.append(None)
        menuItems.append(rumps.MenuItem("Quit Docker Menu", lambda _: rumps.quit_application(_)))
        self.menu.clear()
        self.menu = menuItems

    def updateContainers(self, sender):
        for container in self.__containers.values():
            print(container.getId())
            container.update()
