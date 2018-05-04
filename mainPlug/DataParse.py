
import csv
from UseCommunication import Communicate
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsHeatmapRenderer, QgsColorRampShader, QgsVectorGradientColorRampV2

from PyQt4.QtGui import QColor
import random
import re


class IOParse:

    def __init__(self, path, iface):
        self.iface = iface
        self.path = path
        self.com = Communicate(self.iface)
        try:
            self.csvFile = open(path, 'rb')
        except IOError:
            self.com.error(Bold="IOerror", String="Could not load given File", level=2)
        except:
            self.com.error(Bold="Unknown Error", String="An Unknown Error occured (See log for details", level=2)
            self.com.log("IOPARSE Encountered an Unknown error attempting to initialize self.csvFile", level=2)
        self.Values = 0
        self.ValueList = []

        self.LayerList = []

    def ReadFile(self):
        reader = csv.reader(self.csvFile)
        self.com.log(str(reader), level=0)
        """
        Assume First row is the Values, Each row after that is each data point
        
        Using a Key pair store Within a list
        would look like
        
        [{"lat" : value, "Long" : value ... }, {"lat" : Value, "Long" : value ...},...]
        
        Current input looks like:
        ["lat", "long,....],
        [132, 1322, ...],
        [...],...
        """
        """
        
        for idx, val in enumerate(reader):
            for idxi, vali in enumerate(val):
                if idx == 0:
                    FinalOutput.append(vali)
                else:
                    FinalOutput[idx-1]"""


        readerVal = []
        for i in reader:
            readerVal.append(i)
        self.Values = len(readerVal[0]) - 2
        for idx, val in enumerate(readerVal[0]):
            if idx != 0 and idx != 1 and val != 'ID' or val != 'id' or val != 'Id' or val != 'iD':
                self.ValueList.append(str(val))

        self.add_layer()

    def add_layer(self):
        fPath = 'file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s' % (self.path, 'EPSG:4326', ',', 'Longitude', 'Latitude', '.')
        for idx, val in enumerate(self.ValueList):
            self.LayerList.append(QgsVectorLayer(fPath, val, "delimitedtext"))

        for i in self.LayerList:
            QgsMapLayerRegistry.instance().addMapLayer(i)

        # Get Layers
        p = QgsMapLayerRegistry.instance().mapLayers()
        Long = re.compile("Longitude", re.IGNORECASE)
        Lat = re.compile("Latitude", re.IGNORECASE)
        ID = re.compile("ID", re.IGNORECASE)

        for i in self.LayerList:
            self.com.log(str(i), level=0)

        for i in p.keys():
            if Long.match(i) or Lat.match(i) or ID.match(i):
                QgsMapLayerRegistry.instance().removeMapLayer(i)

        self.color_layers()

    def color_layers(self):
        p = QgsMapLayerRegistry.instance().mapLayers()

        regex = re.compile("\n?(\D*)\d*\n?")


        for key, val in p.iteritems():
            renderer = QgsHeatmapRenderer()
            a = regex.match(key)

            fcn = QgsVectorGradientColorRampV2()

            renderer.setWeightExpression(a.group(1))
            fcn.setColor1(QColor(255, 255, 255, 0))
            fcn.setColor2(QColor(random.randint(0, 100),random.randint(50, 255), random.randint(50, 255), 255))

            renderer.setColorRamp(fcn)
            renderer.setRenderQuality(1) #Max out the quality

            val.setRendererV2(renderer)
