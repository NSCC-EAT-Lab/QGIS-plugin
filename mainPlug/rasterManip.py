from qgis.core import QgsRasterLayer, QgsPoint, QgsRaster, QgsMessageLog
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry


"""
    NDVI = (NIR - Red) / (NIR + RED)
    
    Per pixel Calculation on two layers
    
    Color Ramp based on the Calculated pixel.
"""
import gc

class RasterManip:

    def __init__(self, iface):

        self.iface = iface

        # print(rLayer.renderer().type())

    def return_dataset(self, X, Y, rLayer):
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
        ident = rLayer.dataProvider().identify(QgsPoint(X, Y), QgsRaster.IdentifyFormatValue)
        if ident.isValid():
            return ident.results()
        return ident.results()

    def do_ndvi_calc(self, DataSet, DataSet2=None):
        """
        TODO: MAKE THIS CAPABLE OF TAKING TWO DATASETS AND SPITTING BACK OUT A NORMALIZED DATASET
        To per pixel Calculations to measure NDVI of 1 multiband image or two Single-band-grey images
        :param DataSet: Mandatory, Single or multiband image
        :param DataSet2: Optional, Singleband Image
        :return: Resulting Calculated NDVI normalized dataset
        """
        resul = []
        # Single raster
        if DataSet2 is None:
            for i in DataSet:
                if i is not None:
                    a = (i.get(3) - i.get(1)) / (i.get(3) + i.get(1))

                    resul.append(a)
                else:
                    resul.append(-9999)
                return resul
        # Multi raster
        else:

            for idx, val in enumerate(DataSet):
                # if val is not None:

                    a = (val.get(1) - DataSet2[idx].get(1)) / (val.get(1) + DataSet2[idx].get(1))

                    # print a
                    resul.append(a)
                #else:
                   # resul.append(-9999)
            # print resul
            gc.collect()
            return resul

    def Processing_ndvi_calc(self, rLayer1, rLayer2, path):

        path = path

        r1 = QgsRasterCalculatorEntry()
        r2 = QgsRasterCalculatorEntry()

        r1.ref = "rLayer@1"
        r2.ref = "rLayer@2"

        r1.raster = rLayer1
        r2.raster = rLayer2

        r1.bandNumber = 1
        r2.bandNumber = 1

        entries = [r1, r2]

        expression = "(\"{0}\"-\"{1}\")/(\"{2}\"+\"{3}\")".format(r1.ref, r2.ref, r1.ref, r2.ref)

        a = QgsRasterCalculator(expression, path, 'GTiff', rLayer1.extent(), rLayer1.width(), rLayer1.height(), entries)

        a.processCalculation()
        QgsMessageLog.logMessage("MultiRaster Log:" + str(a.Result), "DeadBeef", level=QgsMessageLog.INFO)

