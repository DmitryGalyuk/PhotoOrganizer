import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import filedialog
from ui import Event

class FolderSelector(ttk.Button):
    def __init__(self, master=None, path=Path.home(), **kw):
        super().__init__(master=master, **kw)
        self.path = path

        self.configure(text=self._folderFromPath(path))
        self.configure(command=self._pressed)
        
    def _folderFromPath(self, path):
        return Path(path).parts[-1]

    def _pressed(self):
        
        folder = filedialog.askdirectory(initialdir=self.path)
        if folder: 
            self.path = folder
            self.configure(text=self._folderFromPath(self.path))
            self.event_generate(Event, data=self.path)
