import tkinter as tk
from tkinter import ttk
from photo import Photo
import os
import concurrent.futures as cf


class ImageList(ttk.Frame):

    def __init__(self, master=None, orient=tk.VERTICAL, path=None, **kw):
        super().__init__(master=master, **kw)

        self.canvas = tk.Canvas(self)
        self.orient = orient
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.path = path

        if orient == tk.VERTICAL:
            scroll = ttk.Scrollbar(self, orient=tk.VERTICAL)
            scroll.pack(side=tk.RIGHT,fill=tk.Y)
            scroll.config(command=self.canvas.yview)
            self.canvas.config(yscrollcommand=scroll.set)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
            scroll.pack(side=tk.BOTTOM,fill=tk.X)
            scroll.config(command=self.canvas.xview)
            self.canvas.config(xscrollcommand=scroll.set)
            self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def renderImages(self):
        pathes = []
        for file in os.listdir(self.path):
            pathes.append(os.path.join(self.path, file))

        size = self.canvas.winfo_width() if self.orient==tk.VERTICAL else self.canvas.winfo_height()

        self.photos = [ ]

        with cf.ThreadPoolExecutor() as executor:
            self.photos = [f.result() for f in cf.as_completed([ executor.submit(Photo, path) for path in pathes]) ]

        self.resizeThumbs((size,size))

        offset = padding = 20
        for photo in self.photos:
            if self.orient==tk.VERTICAL:
                self.canvas.create_image(10, offset, anchor=tk.NW, image=photo.imgTk())
                offset += photo.thumbHeight + padding
            else:
                self.canvas.create_image(offset, 10, anchor=tk.NW, image=photo.imgTk())
                offset += photo.thumbWidth + padding

        if self.orient==tk.HORIZONTAL:
            self.canvas.config(scrollregion=(0,0, offset, size+padding))
        else:
            self.canvas.config(scrollregion=(0,0, size+padding, offset))

    def resizeThumbs(self, boxToFit):
          with cf.ThreadPoolExecutor() as executor:
            cf.wait([ executor.submit(photo.resize, boxToFit[0], boxToFit[0]) for photo in self.photos])
      

    def _on_mousewheel(self, event):
        if self.orient == tk.VERTICAL:
            self.canvas.yview_scroll(-1*(event.delta), "units")
        else:
            self.canvas.xview_scroll(-1*(event.delta), "units")

