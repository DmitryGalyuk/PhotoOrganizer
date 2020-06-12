import tkinter as tk
from tkinter import ttk
from photo import Photo
import os
import concurrent.futures


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
        print("rendering")
        pathes = []
        for file in os.listdir(self.path):
            pathes.append(os.path.join(self.path, file))

        offset = 20
        size = self.canvas.winfo_width() if self.orient==tk.VERTICAL else self.canvas.winfo_height()

        self.photos = [ Photo(path) for path in pathes[:3] ]

        futurePhotos = None
        resizedPhotos = []
        print("photos loaded")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futurePhotos = [ executor.submit(resPhoto, photo, size, size) for photo in self.photos ]
            print("submitted")
            for f in concurrent.futures.as_completed(futurePhotos):
                try:
                    print("before calling result")
                    f.result()
                except Exception as identifier:
                    print(identifier)
                    raise
                else:
                    print(len(resPhoto))
                

        # for photo in self.photos:
        for photo in resizedPhotos:
            # photo.resize(size-40, size-40)
            if self.orient==tk.VERTICAL:
                self.canvas.create_image(10, offset, anchor=tk.NW, image=photo.imageTk)
                offset += photo.thumbHeight+20
                self.canvas.config(scrollregion=(0,0,500,offset))
            else:
                self.canvas.create_image(offset, 10, anchor=tk.NW, image=photo.imageTk)
                offset += photo.thumbWidth+20
                self.canvas.config(scrollregion=(0,0,offset,500))
        
        print("done")
        
    def _on_mousewheel(self, event):
        if self.orient == tk.VERTICAL:
            self.canvas.yview_scroll(-1*(event.delta), "units")
        else:
            self.canvas.xview_scroll(-1*(event.delta), "units")

def resPhoto(photo, x,y):
    print("start resizing")
    photo.resize(x,y)
    print("resized")