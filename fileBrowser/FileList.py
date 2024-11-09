import os
from posix import DirEntry

class FileList():
    def __init__(self, path):
        self.path = path

    # geet list of DirEntry object,
    # with DirEntry object, we can get the name and type, 
    #                       we can also get the path of it
    #                       which we can use to assign the ListItem 
    def getEntryList(self) -> list:
        entryList = []
        with os.scandir(self.path) as entries:
            for entry in entries:
                entryList.append(entry)
        return entryList

    # get file type
    # TODO: optimize this for more variety of functions not just provide string
    def getEntryType(self, entry: DirEntry) -> str:
        if entry.is_file():
            return "File "
        else:
            return "Dir "

    # create a label to assign to ListItem 
    def getLabel(self, entry: DirEntry) -> str:
        return self.getEntryType(entry) + entry.name



