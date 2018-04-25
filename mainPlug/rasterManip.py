
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
        Return back the Results of a XY Cordnate pair
        :param X: X Co-ordnate
        :param Y: Y Co-Ordnate
        :return: The Tuple containing the values from the raster
        """
        """
            
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



    def do_ndvi_calc(self, DataSet, DataSet2=None):
        """
        TODO: MAKE THIS CAPABLE OF TAKING TWO DATASETS AND SPITTING BACK OUT A NORMALIZED DATASET
        To per pixel Calculations to measure NDVI of 1 multiband image or two Singlebandgrey images
        :param DataSet: Mandatory, Single or multiband image
        :param DataSet2: Optional, Singleband Image
        :return: Resulting Calculated NDVI normalized dataset
        """
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

