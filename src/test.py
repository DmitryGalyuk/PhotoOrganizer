from tkinter import *
from PIL import ImageGrab
import cStringIO, base64, time, threading

box = (0,0,500,500) #x,x,width,height
MyImage = ImageGrab.grab(box)

fp = cStringIO.StringIO()
MyImage.save(fp, 'GIF')
MyPhotoImage = PhotoImage(data=base64.encodestring(fp.getvalue()))
Picturelabel = Label(BalanceFrame, image=MyPhotoImage)
Picturelabel.grid(row=3, column=2, columnspan=3)

class PictureThread(threading.Thread):
    def run(self):
        while True:
            box = (0,0,500,500) #x,x,width,height
            MyImage = ImageGrab.grab(box)

            fp = cStringIO.StringIO()
            MyImage.save(fp, 'GIF')
            MyPhotoImage = PhotoImage(data=base64.encodestring(fp.getvalue()))

            time.sleep(5)
            Picturelabel.image = MyPhotoImage 

PictureThread().start()

window.mainloop()