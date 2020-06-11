import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import os
import math as math
from photo import Photo


class Application():
    def __init__(self):
        self.root = tk.Tk()
        self.configData()
        self.create_widgets()  
        self.root.mainloop()

    def configData(self):
        self.d = tk.StringVar()

        path = "/Users/dmitrygalyuk/Dropbox/Projects/py/TestApp/photos"
        self.pathes = []
        for file in os.listdir(path):
            self.pathes.append(os.path.join(path, file))

        self.photos = [Photo(self.pathes[0]),]


    def create_widgets(self):
        self.columns = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.columns.configure(sashrelief = tk.RAISED, sashwidth=5, sashpad=2)
        self.columns.pack(fill=tk.BOTH, expand=True)

        self.leftPane = ttk.Frame(self.columns)
        self.centerRows = tk.PanedWindow(self.columns, orient=tk.VERTICAL)

        self.leftTree = ttk.Treeview(self.leftPane)
        self.leftPane.bind("<Configure>", self.resizeTree)
        self.leftTree.bind('<<TreeviewSelect>>', self.treeItemSelected)
        self.leftTree.pack(fill=tk.BOTH, expand=True)
        self.thumbs = [ Photo(path) for path in self.pathes ]
        
        self.populateLeftTree()
        
        self.imageFrame = ttk.Frame(self.centerRows)
        self.imageFrame.bind("<Configure>", self.resizeImages)
        self.imageFrame.pack(expand=True, fill=tk.BOTH)

        self.buttonsFrame = ttk.Frame(self.columns)
        self.quit = ttk.Button(self.buttonsFrame, text="QUIT", command=self.root.destroy)
        self.quit.pack(side=tk.BOTTOM)
        self.buttonsFrame.pack()

        self.columns.add(self.leftPane)
        self.columns.add(self.centerRows)
        self.centerRows.add(self.imageFrame, stretch="always")
        self.centerRows.add(self.buttonsFrame, stretch="never")

        self.root.geometry("700x700")

        self.renderImages()

    def renderImages(self):
        for c in self.imageFrame.winfo_children(): c.destroy()
        photosCount = len(self.photos)
        squareSize = math.ceil(math.sqrt(photosCount))

        rowNum = colNum = 0
        for x in range(squareSize):
            for y in range(squareSize):
                i = x*squareSize+y
                if not i<photosCount: return
                label = ttk.Label(self.imageFrame, image=self.photos[i].imageTk)
                label.grid(row=x, column=y, sticky=tk.NSEW)
                label.config(border=2, relief=tk.RAISED)
        
        for i in range(squareSize): 
            self.imageFrame.rowconfigure(i, weight=1)
            self.imageFrame.columnconfigure(i, weight=1)
    
    def treeItemSelected(self, event):
        self.photos = [ Photo(path) for path in self.leftTree.selection() ]
        self.renderImages()
    
    def populateLeftTree(self, size=300):
        self.leftTree.delete( *self.leftTree.get_children("") )
        style = ttk.Style(self.root)
        style.configure('Treeview', rowheight=size)
        for thumb in self.thumbs:
            thumb.resize(size, size)
            self.leftTree.insert("", tk.END, thumb.path, open=True, text="", value=thumb.path, image = thumb.imageTk)


    def resizeTree(self, event):
        self.populateLeftTree( event.widget.winfo_width() )
    
    def resizeImages(self, event):
        sqSize=math.ceil(math.sqrt(len(self.photos)))
        for photo in self.photos:
            photo.resize(event.widget.winfo_width()//sqSize, event.widget.winfo_height()//sqSize)
        self.renderImages()
    
    def _printEvent(self, event):
        print(event)

Application()