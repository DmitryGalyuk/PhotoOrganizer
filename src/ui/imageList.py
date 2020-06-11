import tkinter as tk
from tkinter import ttk
from photo import Photo
import os


class ImageList(ttk.Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.canvas = tk.Canvas(self)
        self.vscroll = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.vscroll.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vscroll.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def renderImages(self):
        
        path = "/Users/dmitrygalyuk/Dropbox/Projects/py/TestApp/photos"
        # path = "/Users/dmitrygalyuk/Downloads/Favorites"
        pathes = []
        for file in os.listdir(path):
            pathes.append(os.path.join(path, file))

        self.photos = [ Photo(path) for path in pathes[20:25] ]

        offset = 20
        wid = self.canvas.winfo_width()

        for photo in self.photos:
            photo.resize(wid-40, wid-40)
            self.canvas.create_image(10, offset, anchor=tk.NW, image=photo.imageTk)
            offset += photo.thumbHeight+20
        
        self.canvas.config(scrollregion=(0,0,500,offset))
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta), "units")