import os
from posix import DirEntry

class FileList():
    def __init__(self, path):
        self.path = path
        self.tree = dict() 

    # geet list of DirEntry object,
    # with DirEntry object, we can get the name and type, 
    #                       we can also get the path of it
    #                       which we can use to assign the ListItem 

    # tree is in the form of {directory : list of entries, subdirectory : list of entires in subdirectory, subdirectory2...}
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

    def getDirList(self):
        entryList = self.getEntryList()
        return [entry for entry in entryList if entry.is_dir()]
    

    def searchDir(self,current_depth_relative=0,max_depth=2):
        '''recursively searches files downwards to a max depth'''
        if current_depth_relative <= max_depth:
            dirList = self.getDirList()
            self.tree[self.path] = [entry for entry in self.getEntryList()]

            #creating new FileList class based on new path
            for Dir in dirList:
                newpath = os.path.join(os.getcwd(),Dir)
                subDir = FileList(newpath)
                subDir.searchDir(current_depth_relative + 1, max_depth)
                self.tree.update(subDir.tree)

        

    
if __name__ == "__main__":
    test = FileList(os.path.join(os.getcwd(),"hackUMass7-fileBrowser","Testing"))
    test.searchDir()
    print(test.tree)

