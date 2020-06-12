from datetime import datetime
from pathlib import Path

def listPhotosDates(dir):
    return { path.absolute(): datetime.fromtimestamp(path.stat.st_mtime) 
            for path in Path(dir).iterdir() 
            if path.suffix in [".jpg", ".jpeg"]
    }
    Path().res