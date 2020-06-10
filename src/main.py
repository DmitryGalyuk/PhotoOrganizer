from ui.mainWindow import MainWindow
from config import Config

with Config() as config:
    window = MainWindow(config)
    window.showUI()
