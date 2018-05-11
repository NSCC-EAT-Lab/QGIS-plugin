
from processing.core.Processing import Processing
from processing.tools import *
from UseCommunication import Communicate
from qgis.core import QgsVectorLayer


# from qgis.core import QgsPro

class interp():
    def __init__(self, pointLayer, iface):
        Processing.initialize()
        self.iface = iface
        self.com = Communicate(self.iface)
        self.pLayer = pointLayer
        self.PredictionLayer = QgsVectorLayer()
        self.VarianceLayer = QgsVectorLayer()

    def run_Output(self):
        alg = 'saga:simplekriging'

        layer = self.pLayer
        ext = layer.extent()

        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()

        coords = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)



        params = {"POINTS": self.pLayer, "FIELD": self.pLayer.name(), "TQUALITY": 0, "LOG": False,
                  "BLOCK": False,
                  "DBLOCK": 1, "VAR_MAXDIST": -1, "VAR_NCLASSES": 100, "VAR_NSKIP": 1, "VAR_MODEL": "a+b*x",
                  "OUTPUT_EXTENT": coords, "TARGET_USER_SIZE": 0.000001, "TARGET_USER_FITS": 0,
                  "SEARCH_RANGE": 0, "SEARCH_RADIUS": 1000, "SEARCH_POINTS_ALL": 0, "SEARCH_POINTS_MIN": 4,
                  "SEARCH_POINTS_MAX": 20, "SEARCH_DIRECTION": 0, "PREDICTION": self.PredictionLayer, "VARIANCE": self.VarianceLayer}

        # params = {"POINTS": iface.activeLayer(), "FIELD": iface.activeLayer().name(), "TQUALITY": 0, "LOG": False, "BLOCK": False,
        #            "DBLOCK": 1, "TARGET_USER_SIZE": 0.000001}

        processing.runalg(alg, params)

    def get_PredictionLayer(self):
        return self.PredictionLayer

    def get_VarianceLayer(self):
        return self.VarianceLayer