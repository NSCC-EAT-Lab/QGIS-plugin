
from qgis.core import QgsRasterLayer

class RasterManip:

    def __init__(self, rLayer):
        self.rLayer = rLayer
        print(rLayer.renderer().type())