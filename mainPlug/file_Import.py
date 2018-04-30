from PyQt4.QtCore import QFileInfo
from qgis.core import QgsRasterLayer, QgsMessageLog


class FileImport:

    def __init__(self):
        self.filePath = ''
        self.fileInfo = None
        self.baseName = None
        self.rLayer = None

    def file_input(self, path):
        """
        Set the path and Setup the File to be used later
        :param path: Path to the file you wish to use
        :return: None
        """
        self.filePath = path
        self.fileInfo = QFileInfo(self.filePath)
        self.baseName = self.fileInfo.baseName()
        self.check_file_type()

    def check_file_type(self):
        """
        Validate the File type as a Valid Raster layer
        :return: None
        """
        self.rLayer = QgsRasterLayer(self.filePath, self.baseName)
        if not self.rLayer.isValid():
            print("Layer Failed to load")
            self.rLayer = None
            QgsMessageLog.logMessage("Check File Type Error: Layer Invalid", level=QgsMessageLog.CRITICAL)
            raise IOError
    def get_rLayer(self):
        """
        Get the rLayer
        :return: rLayer Obj
        """
        return self.rLayer
