import tkinter as tk
from tkinter import ttk
from photo import Photo, scaleSize
import os
import concurrent.futures as cf
import queue


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
        def loadAndResize(photo, size):
            p = Photo(p)
            p.resize(size, size)
            return p

        def renderPhotoAtIndex(photo, offset):
            if self.orient==tk.VERTICAL:
                self.canvas.create_image(10, offset, anchor=tk.NW, image=photo.imgTk())
            else:
                self.canvas.create_image(offset, 10, anchor=tk.NW, image=photo.imgTk())

        pathes = []
        for file in os.listdir(self.path):
            pathes.append(os.path.join(self.path, file))

        size = self.canvas.winfo_width() if self.orient==tk.VERTICAL else self.canvas.winfo_height()

        self.photos = [ ]

        mainThreadQueue = queue.Queue()
        with cf.ThreadPoolExecutor() as executor:
            self.photos = [f.result() for f in cf.as_completed([ executor.submit(Photo, path) for path in pathes]) ]

            photoOffset = thumbOffsets(self.photos, (size,size), self.orient, 20)
            if self.orient==tk.HORIZONTAL:
                self.canvas.config(scrollregion=(0,0, photoOffset[self.photos[-1]], size+50))
            else:
                self.canvas.config(scrollregion=(0,0, size+50, photoOffset[self.photos[-1]]))

            # futurePhotos = [ executor.submit(loadAndResize, path, size) for path in pathes ]
            futurePhotos = {executor.submit(
                photoResizeWithCallback, 
                    photo, size, size, mainThreadQueue, renderPhotoAtIndex, photoOffset[photo]
                ): photo for photo in self.photos}


            for i in range(len(self.photos)):
                mainThreadQueue.get(True)()
                i += 1


              

    
    
            
        
    def _on_mousewheel(self, event):
        if self.orient == tk.VERTICAL:
            self.canvas.yview_scroll(-1*(event.delta), "units")
        else:
            self.canvas.xview_scroll(-1*(event.delta), "units")

def photoResizeWithCallback(photo, w, h, queue, callback, offset):
    photo.resize(w,h)
    queue.put(lambda: callback(photo, offset))

def thumbOffsets(photos, boxToFit, orient, padding):
    result = {}
    offset = 0
    for p in photos:
        offset += padding
        thumbSize = scaleSize((p.originalWidth, p.originalHeight), boxToFit)
        result[p] = offset
        offset += (thumbSize[0] if orient==tk.HORIZONTAL else thumbSize[1])
    return result
    
