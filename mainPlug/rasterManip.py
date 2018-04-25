
from qgis.core import QgsRasterLayer, QgsPoint, QgsRaster

"""
    NDVI = (NIR - Red) / (NIR + RED)
    
    Per pixel Calculation on two layers
    
    Color Ramp based on the Calculated pixel.
"""

class RasterManip:

    def __init__(self, rLayer, iface):

        self.rLayer = rLayer
        self.iface = iface
        print(rLayer.renderer().type())

    def return_dataset(self, X, Y):
        """
            Calculate the Specified Pixels NDVI Value
            TODO: Change this later to a more extendable format
        """

        """ 
        This Outputs all of the Bands
        Using a for loop, we can very easily check each point... though... How will we limit it's size?
        """
        ident = self.rLayer.dataProvider().identify(QgsPoint(X, Y), QgsRaster.IdentifyFormatValue)

        if ident.isValid():
            return ident.results()
        return ident.results()


    # TODO: Figure out why this crashing the plugin

    def do_ndvi_calc(self, DataSet, DataSet2=None):
        resul = []

        if DataSet2 is None:
            for i in DataSet:
                a = (i.get(4) - i.get(1)) / (i.get(4) + i.get(1))
                resul.append(a)
            return resul
        else:
            i = 0
            j = 0
            while True:
                a = DataSet.get(1)
                b = DataSet2.get(1)
                c = (a - b) / (a + b)
                resul.append(c)
                if i != len(DataSet) & j != len(DataSet2):
                    i += 1
                    j += 1
                else:
                    break

            return resul

