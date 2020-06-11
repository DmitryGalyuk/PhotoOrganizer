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

        imageList = ImageList(sourcePanel, relief=tk.SUNKEN)
        imageList.pack(fill=tk.BOTH, expand=True, pady=2, padx=2)
        self._root.after(500, imageList.renderImages)

        framePhotos = ttk.Frame(columns)
        framePhotos.pack(fill=tk.BOTH, expand=True)

        rightLabel = ttk.Label(columns, text="my fance label")
        rightLabel.pack(pady=2, padx=2)

        columns.add(sourcePanel)
        columns.add(framePhotos, sticky=tk.NSEW, stretch="middle")
        columns.add(rightLabel, stretch="middle")

        columns

        columns.paneconfigure(sourcePanel, width=self.config["UI"]["leftColumnWidth"])


    def getChangeHandler(self, section, option, widgetProp):
        return lambda event: self.config.set(section, option, getattr(event.widget, widgetProp))
