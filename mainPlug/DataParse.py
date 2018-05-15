"""
/*
Implement CSV Data set functions for Opening reading and passing data internally
*/
"""

import csv
import random
import re

from PyQt4.QtGui import QColor
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsHeatmapRenderer, QgsVectorGradientColorRampV2

from UseCommunication import Communicate


class IOParse:
    """
    /*
    Implement CSV Data set functions for Opening reading and passing data internally
    */
    """
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
        """
        Read the CSV, Bringing it in to be worked on. Appending to a Value list for later work
        :return:
        """
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
        """
        Add the Layers to the screen, This function assigns each layer to the screen and creates a Layer List to later
        match the layer weight

        :return: None
        """
        # TODO: Add in smart deliminator and Decimal assignment, NOTE regex might not work due to this being a bit more complex
        fPath = 'file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s' % (self.path, 'EPSG:4326', ',',
                                                                                   'Longitude', 'Latitude', '.')

        file = open(self.path, 'r')
        CommaSep = re.compile("\w*(\,)", re.IGNORECASE)
        decimal = re.compile("\d(\.)", re.IGNORECASE)
        issue = 0

        try:
            l1 = file.readline()
            l2 = file.readline()
            self.com.log(str(l1), level=0)
            self.com.log(str(l2), level=0)

            if CommaSep.match(l1) == '' or CommaSep.match(l1) is None:
                issue = 1
                raise IOError

            if decimal.match(l2) == '' or decimal.match(l2) is None:
                issue = 2
                raise IOError

        except IOError:
            # Fail Silently (Due to some current issues where in the Decimal is not correctly noticed, causing an issue
            if issue == 1:
                pass
                # self.com.error(Bold="DataSampleError:", String="Soil sample data separator is not , (comma)", level=2,
                #                duration=6)
            elif issue == 2:
                pass
                # self.com.error(Bold="DataSampleError:", String="Soil sample Data decimal mark is not . (Period)",
                #                level=2, duration=6)

        for idx, val in enumerate(self.ValueList):
            self.LayerList.append(QgsVectorLayer(fPath, val, "delimitedtext"))

        for i in self.LayerList:
            QgsMapLayerRegistry.instance().addMapLayer(i)

        # Get Layers
        p = QgsMapLayerRegistry.instance().mapLayers()

        longitude = re.compile("Longitude", re.IGNORECASE)
        latitude = re.compile("Latitude", re.IGNORECASE)
        id = re.compile("ID", re.IGNORECASE)

        for i in self.LayerList:
            self.com.log(str(i), level=0)

        for i in p.keys():
            if longitude.match(i) or latitude.match(i) or id.match(i):
                QgsMapLayerRegistry.instance().removeMapLayer(i)

        self.color_layers()

    def color_layers(self):
        """
        Attempts to assign and color each layer after changing it's renderer to a heatmap renderer
        NOTE: This uses a Random sequence for color grading

        TODO: Update color grading to generally output more readable colors Possibly make higher values have more radius?
        :return: None
        """
        p = QgsMapLayerRegistry.instance().mapLayers()

        regex = re.compile("\n?(\D*)\d*\n?")

        for key, val in p.iteritems():
            renderer = QgsHeatmapRenderer()
            a = regex.match(key)

            fcn = QgsVectorGradientColorRampV2()

            renderer.setWeightExpression(a.group(1))
            fcn.setColor1(QColor(255, 255, 255, 0))
            fcn.setColor2(QColor(random.randint(0, 100), random.randint(50, 255), random.randint(50, 255), 255))

            renderer.setColorRamp(fcn)
            renderer.setRenderQuality(1)  # Max out the quality

            val.setRendererV2(renderer)
