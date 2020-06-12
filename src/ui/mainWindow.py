import tkinter as tk
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
        self._root.bind("<Configure>", lambda event: self.config.set("UI", "geometry", self._root.geometry()))

        self._createWidgets()
        self._root.mainloop()


    def _createWidgets(self):
        columns = tk.PanedWindow(self._root, orient=tk.HORIZONTAL)
        columns.configure(sashrelief = tk.RAISED, sashwidth=5, sashpad=2)
        columns.pack(fill=tk.BOTH, expand=True)
        columns.bind("<ButtonRelease-1>", lambda event: (print(sourcePanel.winfo_width())))

        sourcePanel = ttk.Frame(columns)
        sourcePanel.bind("<Configure>", lambda event: self.config.set("UI","leftColumnWidth", str(event.width)))       
        sourcePanel.pack(fill=tk.BOTH, expand=True)

        sourceFolder = FolderSelector(sourcePanel, path=self.config["Pathes"]["source"])
        sourceFolder.bind(Event, self.getChangeHandler("Pathes", "source", "path"))
        sourceFolder.pack(fill=tk.X, expand=False, pady=2)

        path = "/Users/dmitrygalyuk/Dropbox/Projects/py/TestApp/photos"
        imageList = ImageList(sourcePanel, relief=tk.SUNKEN, path=path)
        imageList.pack(fill=tk.BOTH, expand=True, pady=2, padx=2)
        self._root.after(2000, imageList.renderImages)

        middlePanes = tk.PanedWindow(columns, orient=tk.VERTICAL)
        middlePanes.pack()

        framePhotos = ttk.Frame(middlePanes)
        framePhotos.pack(fill=tk.BOTH, expand=True)

        path = "/Users/dmitrygalyuk/Downloads/Favorites"
        trashPanel = ttk.Frame(middlePanes)
        trashList = ImageList(trashPanel, orient=tk.HORIZONTAL, path=path)
        trashList.pack(fill=tk.BOTH, expand=True, pady=2, padx=2)
        self._root.after(2000, trashList.renderImages)

        middlePanes.add(framePhotos, stretch="first")
        middlePanes.add(trashPanel, stretch="first")

        rightLabel = ttk.Label(columns, text="my fance label")
        rightLabel.pack(pady=2, padx=2)

        columns.add(sourcePanel)
        columns.add(middlePanes, sticky=tk.NSEW, stretch="middle")
        columns.add(rightLabel, stretch="middle")

        columns

        columns.paneconfigure(sourcePanel, width=self.config["UI"]["leftColumnWidth"])


    def getChangeHandler(self, section, option, widgetProp):
        return lambda event: self.config.set(section, option, getattr(event.widget, widgetProp))
