from PIL import ImageTk, Image, ExifTags, ImageChops
import math

class Photo():
    def __init__(self, path, size=(1000, 1000)):
        self.path = path
        self.originalImage = Image.open(path)
        self.originalImage = fixOrientation(self.originalImage)
        self.originalHeight = self.originalImage.height
        self.originalWidth = self.originalImage.width

        calc = scaleSize((self.originalWidth, self.originalHeight), size)
        self.thumbWidth = calc[0]
        self.thumbHeight = calc[1]
        self.thumb = self.originalImage.copy()
        self.thumb.thumbnail(size)
        self.imageTk = None

    def imgTk(self):
        if self.imageTk is None:
            self.imageTk = ImageTk.PhotoImage(self.thumb)
        return self.imageTk


    def resize(self, w, h):
        if w < 2: return
        t = self.originalImage.copy()
        calc = scaleSize((self.originalWidth, self.originalHeight), (w,h))
        self.thumbWidth = calc[0]
        self.thumbHeight = calc[1]
        t.thumbnail((w,h))
        self.thumb = t
        self.imageTk = None

def fixOrientation(image):
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

def scaleSize(initialSize, boxToFit):
    x, y = map(math.floor, boxToFit)
    if x >= initialSize[0] and y >= initialSize[1]:
        return initialSize

    def round_aspect(number, key):
        return max(min(math.floor(number), math.ceil(number), key=key), 1)

    # preserve aspect ratio
    aspect = initialSize[0] / initialSize[1]
    if x / y >= aspect:
        x = round_aspect(y * aspect, key=lambda n: abs(aspect - n / y))
    else:
        y = round_aspect(x / aspect, key=lambda n: abs(aspect - x / n))
    return (x, y)