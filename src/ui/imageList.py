import tkinter as tk
from tkinter import ttk
from photo import Photo
import os
import concurrent.futures as cf
from datetime import datetime
from pathlib import Path


class ImageList(ttk.Frame):

    def __init__(self, master=None, name=None, orient=tk.VERTICAL, path=None, padding=20, **kw):
        super().__init__(master=master, **kw)

        if not name: raise ValueError("name is required")
        if not path: raise ValueError("path is required")
        self.name = name
        self.orient = orient
        self.path = path
        self.padding = padding
        self.scrollRegionSet = False

        self.canvas = tk.Canvas(self)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.oldViewPoint = self.canvas.yview() if self.orient==tk.VERTICAL else self.canvas.xview()

        self.pathToDate = { str(p): datetime.fromtimestamp(p.stat().st_mtime) 
            for p in Path(path).iterdir() 
            if p.is_file() and p.suffix in [".jpg", ".jpeg", ".png"]
        }

        def getScrollHandler(default):
            def handler(*args):
                # default(*args)
                newViewPoint = (float(args[0]),float(args[1]))
                if self.oldViewPoint != newViewPoint:
                    self.renderImages()
                    self.oldViewPoint = newViewPoint
            return handler

        if orient == tk.VERTICAL:
            scroll = ttk.Scrollbar(self, orient=tk.VERTICAL)
            scroll.pack(side=tk.RIGHT,fill=tk.Y)
            scroll.config(command=self.canvas.yview)
            self.canvas.config(yscrollcommand=getScrollHandler(scroll.set))
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
            scroll.pack(side=tk.BOTTOM,fill=tk.X)
            scroll.config(command=self.canvas.xview)
            self.canvas.config(xscrollcommand=getScrollHandler(scroll.set))
            self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            

    def renderImages(self):
        padding = 20
        size = self._thumbSize()
        approxTotalLength = len(self.pathToDate) * self._thumbSize()

        if not self.scrollRegionSet:
            if self.orient == tk.VERTICAL:
                self.canvas.config(scrollregion=(0,0, self._thumbSize()+self.padding, approxTotalLength))
            else:
                self.canvas.config(scrollregion=(0,0, approxTotalLength, self._thumbSize()+self.padding)) 
            self.scrollRegionSet = True

        viewPoint = self.canvas.yview() if self.orient==tk.VERTICAL else self.canvas.xview()
        firstIndex = int(len(self.pathToDate) * viewPoint[0])
        lastIndex = int(len(self.pathToDate) * viewPoint[1])


        self.photos = [ ]
        with cf.ThreadPoolExecutor(max_workers=10) as executor:
            self.photos = [f.result() for f in cf.as_completed(
                [ executor.submit(Photo, path) for path in 
                    list(self.pathToDate.keys())[firstIndex:lastIndex]
                ]
            )]
            cf.wait([ executor.submit(photo.resize, size-padding,size-padding) for photo in self.photos])

        self.photos = list(reversed(sorted(self.photos, key=lambda p: self.pathToDate[p.path])))

        offset = self.canvas.canvasy(padding) if self.orient==tk.VERTICAL else self.canvas.canvasx(padding)
        for photo in self.photos:
            if self.orient==tk.VERTICAL:
                self.canvas.create_image(10, offset, anchor=tk.NW, image=photo.imgTk())
                offset += photo.thumbHeight + padding
            else:
                self.canvas.create_image(offset, 10, anchor=tk.NW, image=photo.imgTk())
                offset += photo.thumbWidth + padding

        canvas.configure(scrollregion = canvas.bbox("all"))



    def _thumbSize(self):
        return self.canvas.winfo_width() if self.orient==tk.VERTICAL else self.canvas.winfo_height()
      

    def _on_mousewheel(self, event):
        if self.orient == tk.VERTICAL:
            self.canvas.yview_scroll(-1*(event.delta), "units")
        else:
            self.canvas.xview_scroll(-1*(event.delta), "units")

