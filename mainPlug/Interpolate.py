"""
Interpolation Function; Acts as a go between for QGIS's Processing function (SAGA specifically) and the end user,
 Simplifying the process and removing possible user error
"""

from processing.core.Processing import processing
from processing.tools import *
from UseCommunication import Communicate
from qgis.core import QgsVectorLayer

from file_Import import FileImport
import os


# from qgis.core import QgsPro

class interp:
    def __init__(self, pointLayer, iface):
        # processing.initialize()
        self.iface = iface
        self.com = Communicate(self.iface)
        self.pLayer = pointLayer
        self.PredictionLayer = ""
        self.VarianceLayer = ""

    def run_Output(self):
        """
        Run the Simplekriging process Fully automated, To change any of the Run Options, Use the params dict

        If you need help with the algorithm, within the internal Python environment run

from processing.core.Processing import processing
from processing.tools import *
processing.alghelp("saga:simplekriging")  # this should display correct usage

        TODO: Make the output actually go to its own folder (Currently stuck with a escaping problem "\\" )
        :return: None
        """
        alg = 'saga:simplekriging'

        layer = self.pLayer
        ext = layer.extent()

        x_min = ext.xMinimum()
        x_max = ext.xMaximum()
        y_min = ext.yMinimum()
        y_max = ext.yMaximum()

        self.PredictionLayer = os.path.expanduser("~") + "\\" + self.pLayer.name()

        self.com.log(String="Path of File" + self.PredictionLayer + "\n", level=0)

        coords = "%f,%f,%f,%f" % (x_min, x_max, y_min, y_max)

        params = {"POINTS": self.pLayer, "FIELD": self.pLayer.name(), "TQUALITY": 0, "LOG": False,
                  "BLOCK": False,
                  "DBLOCK": 1, "VAR_MAXDIST": -1, "VAR_NCLASSES": 100, "VAR_NSKIP": 1, "VAR_MODEL": "a+b*x",
                  "OUTPUT_EXTENT": coords, "TARGET_USER_SIZE": 0.000001, "TARGET_USER_FITS": 0,
                  "SEARCH_RANGE": 0, "SEARCH_RADIUS": 1000, "SEARCH_POINTS_ALL": 0, "SEARCH_POINTS_MIN": 4,
                  "SEARCH_POINTS_MAX": 20, "SEARCH_DIRECTION": 0, "PREDICTION": self.PredictionLayer}

        # params = {"POINTS": iface.activeLayer(), "FIELD": iface.activeLayer().name(), "TQUALITY": 0, "LOG": False, "BLOCK": False,
        #            "DBLOCK": 1, "TARGET_USER_SIZE": 0.000001}

        processing.runalg(alg, params)

        self.iface.addRasterLayer(self.PredictionLayer + ".tif", self.pLayer.name() + " Prediction")

    def get_PredictionLayer(self):
        """
        Return the prediction layer path
        :return: Path - Str
        """
        return self.PredictionLayer

    def get_VarianceLayer(self):
        """
        Return the variance layer path (Only works if set internally
        :return: Path - Str
        """
        return self.VarianceLayer
