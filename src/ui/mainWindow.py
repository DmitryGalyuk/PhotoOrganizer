from ui.folderSelector import FolderSelector
import tkinter as tk
from tkinter import ttk
from ui import Event


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
        columns= tk.PanedWindow(self._root, orient=tk.HORIZONTAL)
        columns.configure(sashrelief = tk.RAISED, sashwidth=5, sashpad=2)
        columns.pack(fill=tk.BOTH, expand=True)

        sourcePanel= ttk.Frame(columns)
        sourcePanel.bind("<Configure>", lambda event: self.config.set("UI","leftColumnWidth", str(event.width)))       
        sourcePanel.pack()

        sourceFolder = FolderSelector(sourcePanel, path=self.config["Pathes"]["source"])
        sourceFolder.bind(Event, self.getChangeHandler("Pathes", "source", "path"))
        sourceFolder.pack(side=tk.TOP, fill=tk.X, expand=False)

        framePhotos= ttk.Frame(columns)
        framePhotos.pack(fill=tk.BOTH, expand=True)

        columns.add(sourcePanel)
        columns.add(framePhotos, sticky=tk.NSEW)

        columns.paneconfigure(sourcePanel, width=self.config["UI"]["leftColumnWidth"])


    def getChangeHandler(self, section, option, widgetProp):
        return lambda event: self.config.set(section, option, getattr(event.widget, widgetProp))
