from PIL import ImageTk, Image, ExifTags, ImageChops

class Photo():
    def __init__(self, path, size=(1000, 1000)):
        self.path = path
        self.image = Image.open(path)
        self.image = self.fixOrientation(self.image)
        self.originalHeight = self.image.height
        self.originalWidth = self.image.width
        self.image.thumbnail(size)
        self.thumbHeight = self.image.height
        self.thumbWidth = self.image.width

        self.imageTk = ImageTk.PhotoImage(self.image)


    def resize(self, w, h):
        if w < 2: return
        t = self.image.copy()
        t.thumbnail((w,h))
        self.thumbHeight = t.height
        self.thumbWidth = t.width
        self.imageTk = ImageTk.PhotoImage(t)

    def fixOrientation(self, image):
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break

            exif=dict(image._getexif().items())

            if exif[orientation] == 3:
                image=image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image=image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image=image.rotate(90, expand=True)

            return image
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            return image
 