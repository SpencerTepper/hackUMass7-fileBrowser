import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Label
from textual.widget import Widget
from textual.reactive import reactive
from FileList import FileList

# FIX: cant get the action_go_back working
# the path change, but I cant come up with a way 
# to populate the ListView when it re-composed
# NOTE: Tried async and await, but no impact

# a big widget that is kinda a custom ListView
# adding and refreshing ListView widget when path change
class FileViewer(Widget):
    # reactive path
    # recompose when this is changed
    #   it is changed when we go up and down the depth
    # so it re-render the list of file
    path = reactive(os.getcwd(), recompose= True)
    
    # NOTE:ignore async and await if you want, it just my attempt to fix
    
    # on_ is for actions to run at a certain event

    # mount is when before the app UI render and run, usually to set up bindings, databases, etc
    async def on_mount(self) -> None:
        self.viewer = self.query_one("#viewer", ListView)
        await self.refreshItems()

    # compose is just render
    def compose(self) -> ComposeResult:
        # id is for query_one, which is just a function that is used to refer to a widget,
        #                       changing widget stuff such as FileViewer.path
        yield ListView(id="viewer")

    # a function to add items to the ListView widget,
    # rendering folders and files
    # TODO: add .. folder
    async def refreshItems(self) -> None:
        fileList = FileList(self.path)
        entryList = fileList.getEntryList()

        self.viewer.clear()

        for entry in entryList:
            label = fileList.getLabel(entry)
            item = ListItem(Label(label))
            self.viewer.append(item)

class fileBrowser(App):
    BINDINGS = [("backspace", "go_back", "Go Back"),
                ("q", "exit", "Exit")]
    def compose(self) -> ComposeResult:
        yield Header()
        yield FileViewer()
        yield Footer()

    # go back is just to get the parent path and change the path
    # textual suppose to automatically rerender because viewer.path is using reactive, as refer above
    def action_go_back(self) -> None:
        viewer = self.query_one(FileViewer)
        parrent_path = os.path.dirname(viewer.path)
        if viewer.path != parrent_path: #check if root
            viewer.path = parrent_path

    def action_exit(self) -> None:
        self.exit()
    
if __name__ == "__main__":
    app = fileBrowser()
    app.run()
