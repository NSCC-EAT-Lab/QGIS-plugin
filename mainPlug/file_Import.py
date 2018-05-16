"""
Import Raster images for use Internally
"""
from PyQt4.QtCore import QFileInfo
from qgis.core import QgsRasterLayer

from UseCommunication import Communicate


class FileImport:

    def __init__(self):
        """
        Initialize the File Import Class
        """
        self.com = Communicate()
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
        if path == '':
            self.com.log("FILE PATH EMPTY", 2)
            raise IOError

        self.filePath = path
        self.fileInfo = QFileInfo(self.filePath)
        self.baseName = self.fileInfo.baseName()
        # Ensure that this stays in as this is how the Raster is imported.
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
            self.com.log("Check File Type Error: Layer Invalid", 2)
            raise IOError

    def get_rLayer(self):
        """
        Get the rLayer
        :return: rLayer Obj
        """
        return self.rLayer
