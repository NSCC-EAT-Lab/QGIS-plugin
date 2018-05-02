from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsPoint, QgsRaster
from UseCommunication import Communicate

"""
    NDVI = (NIR - Red) / (NIR + RED)
     
    Per pixel Calculation on two layers 
     
    Color Ramp based on the Calculated pixel. 
"""
import gc


class RasterManip:

    def __init__(self, iface):

        self.iface = iface
        self.com = Communicate(self.iface)

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

                resul.append(a)
            # else:
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


    def RasterCalcMulti_NDVI(self, rLayer1, path, calctype, rLayer2=None, r1Band=None, r2Band=None, rLayer3=None, r3Band=None):
        """
        Calculate any type of NDVI like Calculation from various types of Cameras be they: Multi output, NGB, RGB, NR
        :param rLayer1: first rLayer object
        :param path: path to Output
        :param calctype: Calculation to perform
        :param rLayer2: second rLayer object
        :param r1Band1: band number
        :param r1Band2: band number
        :param r2Band: band Number
        :param band3: band number
        :param band3rLayer: Which rLayer contains the 3rd band
        :return: None
        """
        """
        TODO: Add support for Multiple different Raster types, be they Single Raster (Of NGB, RGB or otherwise) or Multiraster
        
        https://maxmax.com/ndv_historyi.htm
        
        Implement NDVI Red
        NDVI blue
         and ENDVI (Enhanced NDVI)
        """
        path = path
        r1 = QgsRasterCalculatorEntry()
        r2 = QgsRasterCalculatorEntry()
        r3 = QgsRasterCalculatorEntry()

        # Do variable creation
        # TODO: Fix this, it's spaghetti AF
        r1.raster = rLayer1
        r1.bandNumber = r1Band
        r2.bandNumber = r2Band
        r3.bandNumber = r3Band
        r1.ref = 'Input1@1'
        r2.ref = 'Input2@1'
        r3.ref = 'Input3@1'

        if r1Band is None:
            r1.bandNumber = 1
        if rLayer2 is not None:
            r2.raster = rLayer2
            if r2Band is None:
                r2.bandNumber = 1
        if rLayer3 is not None:
            r3.raster = rLayer3
            if r3Band is None:
                r3.bandNumber = 1

        entries = []

        if calctype is None:
            self.com.error(String="Calctype None", level=2)
        elif calctype == "NDVI":
            # This assumes that that rLayer1 is N and rLayer2 is R
            entries.append(r1)
            entries.append(r2)
            expression = "(\"{0}\"-\"{1}\")/(\"{2}\"+\"{3}\")".format(r1.ref, r2.ref, r1.ref, r2.ref)
            a = QgsRasterCalculator(expression, path, 'GTiff', rLayer1.extent(), rLayer1.width(), rLayer1.height(),
                                    entries)
            a.processCalculation()
        elif calctype == "bNDVI":
            # This assumes that rLayer1 in N and rLayer2 is B
            entries.append(r1)
            entries.append(r2)
            expression = "(\"{0}\"-\"{1}\")/(\"{2}\"+\"{3}\")".format(r1.ref, r2.ref, r1.ref, r2.ref)
            a = QgsRasterCalculator(expression, path, 'GTiff', rLayer1.extent(), rLayer1.width(), rLayer1.height(),
                                    entries)
            a.processCalculation()
        elif calctype == "ENDVI":
            # This assumes that rLayer1 is N, rLayer2 is Green and rLayer3 is Blue
            entries.append(r1)
            entries.append(r2)
            entries.append(r3)
            expression = "((\"{0}\"+\"{1}\")-(2*\"{2}\"))/((\"{0}\"+\"{1}\")+(2*\"{2}\"))".format(r1.ref, r2.ref, r3.ref
                                                                                                  )
            a = QgsRasterCalculator(expression, path, 'GTiff', rLayer1.extent(), rLayer1.width(), rLayer1.height(),
                                    entries)
            a.processCalculation()
        else:
            self.com.error(Bold="CalcType Error", String="Unrecognized calctype", level=2)
