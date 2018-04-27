from qgis.core import QgsRasterLayer, QgsPoint, QgsRaster, QgsMessageLog

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
        #Single raster
        if DataSet2 is None:
            for i in DataSet:
                if i is not None:
                    a = (i.get(3) - i.get(1)) / (i.get(3) + i.get(1))
                    QgsMessageLog.logMessage("SingleRaster Log: " + str(a), "DeadBeef", level=QgsMessageLog.INFO)
                    resul.append(a)
                else:
                    resul.append(-9999)
                return resul
        #Multi raster
        else:
            QgsMessageLog.logMessage("DATASET:" + str(DataSet), "DeadBeef", level=QgsMessageLog.CRITICAL)
            for idx, val in enumerate(DataSet):
                #if val is not None:

                    a = (val.get(1) - DataSet2[idx].get(1)) / (val.get(1) + DataSet2[idx].get(1))
                    QgsMessageLog.logMessage("MultiRaster Log: " + str(a), "DeadBeef", level=QgsMessageLog.INFO)
                    # print a
                    resul.append(a)
                #else:
                   # resul.append(-9999)
            # print resul
            gc.collect()
            return resul
