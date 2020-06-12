import tkinter as tk
# import mtTkinter as mtk
from tkinter import ttk
from ui import Event
from ui.folderSelector import FolderSelector
from ui.imageList import ImageList



class MainWindow():

    def __init__(self, config):
        self.config = config

    def showUI(self):
        self._root = tk.Tk()
        self._root.title("Photo Organizer")

        self._root.geometry(self.config["UI"]["geometry"])

        self._createWidgets()

        self._root.bind("<Configure>", lambda event: self.config.set("UI", "geometry", self._root.geometry()))

        def renderImageLists():
            self.imageList.renderImages()
            self.trashList.renderImages()

        self._root.after(500, renderImageLists)


        self._root.mainloop()


    def _createWidgets(self):
        columns = tk.PanedWindow(self._root, orient=tk.HORIZONTAL)
        columns.configure(sashrelief = tk.RAISED, sashwidth=5, sashpad=2)
        columns.pack(fill=tk.BOTH, expand=True)

        sourcePanel = ttk.Frame(columns)
        sourcePanel.pack(fill=tk.BOTH, expand=True)

        sourceFolder = FolderSelector(sourcePanel, path=self.config["Pathes"]["source"])
        sourceFolder.bind(Event, self._getChangeHandler("Pathes", "source", "path"))
        sourceFolder.pack(fill=tk.X, expand=False, pady=2)

        path = "/Users/dmitrygalyuk/Dropbox/Projects/py/TestApp/photos"
        # path = "/Users/dmitrygalyuk/Dropbox/Camera Uploads"
        self.imageList = ImageList(sourcePanel,name="sourceList", relief=tk.SUNKEN, path=path)
        self.imageList.pack(fill=tk.BOTH, expand=True, pady=2, padx=2)
        # self._root.after(500, self.imageList.renderImages)

        middlePanes = tk.PanedWindow(columns, orient=tk.VERTICAL)
        middlePanes.configure(sashrelief = tk.RAISED, sashwidth=5, sashpad=2)
        middlePanes.pack()

        framePhotos = ttk.Frame(middlePanes)
        framePhotos.pack(fill=tk.BOTH, expand=True)

        path = "/Users/dmitrygalyuk/Downloads/Favorites"
        trashPanel = ttk.Frame(middlePanes)
        self.trashList = ImageList(trashPanel, name="trashList", orient=tk.HORIZONTAL, path=path)
        self.trashList.pack(fill=tk.BOTH, expand=True, pady=2, padx=2)

        columns.bind("<ButtonRelease-1>", self._onPaneResize)
        middlePanes.bind("<ButtonRelease-1>", self._onPaneResize)

        middlePanes.add(framePhotos, stretch="first")
        middlePanes.add(trashPanel, stretch="first")

        rightLabel = ttk.Label(columns, text="my fancy label")
        rightLabel.pack(pady=2, padx=2)

        columns.add(sourcePanel)
        columns.add(middlePanes, sticky=tk.NSEW, stretch="middle")
        columns.add(rightLabel, stretch="middle")

        columns.paneconfigure(sourcePanel, width=self.config[self.imageList.name]["width"])
        middlePanes.paneconfigure(trashPanel, height=self.config[self.trashList.name]["height"])

    def _onPaneResize(self, e):
        def allChildren(widget, result=[]):
            children = widget.winfo_children()
            result.extend(children)
            result.extend([allChildren(c, result) for c in children if len(children)])
            return result
        
        lists = [l for l in allChildren(e.widget) if isinstance(l, ImageList)]

        for imgList in lists:
            oldSize = self.config[imgList.name]
            newSize = imgList.winfo_width() if imgList.orient==tk.VERTICAL else imgList.winfo_height()
            if oldSize == newSize: continue

            option = "height" if imgList.orient==tk.HORIZONTAL else "width"
            self.config[imgList.name][option] = str(newSize)
            imgList.renderImages()
         
        
    
    def _getChangeHandler(self, section, option, widgetProp):
        return lambda event: self.config.set(section, option, getattr(event.widget, widgetProp))
