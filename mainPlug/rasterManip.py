from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsPoint, QgsRaster
from UseCommunication import Communicate

import gc


class RasterManip:

    def __init__(self, iface):
        """
        The work horse of the NDVI calculations, named rasterManip due to it's older functions
        :param iface: The iface passed in from mainPlug
        """
        self.iface = iface
        self.com = Communicate(self.iface)

    @staticmethod
    def return_dataset(X, Y, rLayer):
        """
        Return back the Results of a XY Cordnate pair
        :param X: X Co-ordnate
        :param Y: Y Co-Ordnate
        :return: The Tuple containing the values from the raster
        """
        ident = rLayer.dataProvider().identify(
            QgsPoint(X, Y), QgsRaster.IdentifyFormatValue)
        if ident.isValid():
            return ident.results()
        return ident.results()

    @staticmethod
    def do_ndvi_calc(DataSet, DataSet2=None):
        """
        To per pixel Calculations to measure NDVI of 1 multiband image or two Single-band-grey images

        DEPRECATED
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

                a = (val.get(1) - DataSet2[idx].get(1)) / \
                    (val.get(1) + DataSet2[idx].get(1))

                resul.append(a)
            # else:
            gc.collect()
            return resul

    @staticmethod
    def processing_ndvi_calc(rLayer1, rLayer2, path):
        """
        Older deprecated NDVI handler, This is simply the template for the monstrosity that the current one has become
        :param rLayer1: rLayer 1 Object
        :param rLayer2: rLayer 2 Object
        :param path: Path to Output too
        :return: None
        """

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

        expression = "(\"{0}\"-\"{1}\")/(\"{2}\"+\"{3}\")".format(r1.ref,
                                                                  r2.ref, r1.ref, r2.ref)

        a = QgsRasterCalculator(expression, path, 'GTiff', rLayer1.extent(
        ), rLayer1.width(), rLayer1.height(), entries)

        a.processCalculation()

    def rastercalcmulti_ndvi(self, rLayer1, path, calctype, rLayer2=None,
                             r1Band=1, r2Band=1, rLayer3=None, r3Band=1):
        """
        Calculate any type of NDVI like Calculation from various types of Cameras be they: Multi output, NGB, RGB, NR
        :param r1Band: first Raster Layer Band number
        :param rLayer3: third rLayer object
        :param r3Band: third Raster band
        :param rLayer1: first rLayer object
        :param path: path to Output
        :param calctype: Calculation to perform
        :param rLayer2: second rLayer object
        :param r2Band: band Number
        :return: None
        """
        """
        TODO: Add support for Multiple different Raster types, be they Single Raster (Of NGB, RGB or otherwise) or Multiraster

        https://maxmax.com/ndv_historyi.htm

        Implement NDVI Red
        NDVI blue
         and ENDVI (Enhanced NDVI)
        """
        if path == '' or path is None:
            self.com.log(
                "No Path on NDVI calc function, This will likely cause an error", level=2)

        path = path
        r1 = QgsRasterCalculatorEntry()
        r2 = QgsRasterCalculatorEntry()
        r3 = QgsRasterCalculatorEntry()

        exporttype = "GTiff"

        # Do variable creation
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

        if rLayer3 is not None:
            r3.raster = rLayer3

        entries = []

        if calctype is None:
            self.com.error(String="Calctype None", level=2)

        elif calctype == "NDVI":
            # This assumes that that rLayer1 is N and rLayer2 is R
            entries.append(r1)
            entries.append(r2)
            expression = "(\"{0}\"-\"{1}\")/(\"{2}\"+\"{3}\")".format(r1.ref,
                                                                      r2.ref, r1.ref, r2.ref)
            a = QgsRasterCalculator(expression, path, exporttype, rLayer1.extent(), rLayer1.width(), rLayer1.height(),
                                    entries)
            a.processCalculation()

        elif calctype == "bNDVI":
            # This assumes that rLayer1 in N and rLayer2 is B
            entries.append(r1)
            entries.append(r2)
            expression = "(\"{0}\"-\"{1}\")/(\"{2}\"+\"{3}\")".format(r1.ref,
                                                                      r2.ref, r1.ref, r2.ref)
            a = QgsRasterCalculator(expression, path, exporttype, rLayer1.extent(), rLayer1.width(), rLayer1.height(),
                                    entries)
            a.processCalculation()

        elif calctype == "ENDVI":
            # This assumes that rLayer1 is N, rLayer2 is Green and rLayer3 is
            # Blue
            entries.append(r1)
            entries.append(r2)
            entries.append(r3)
            expression = "((\"{0}\"+\"{1}\")-(2*\"{2}\"))/((\"{0}\"+\"{1}\")+(2*\"{2}\"))".format(r1.ref, r2.ref, r3.ref
                                                                                                  )
            a = QgsRasterCalculator(expression, path, exporttype, rLayer1.extent(), rLayer1.width(), rLayer1.height(),
                                    entries)
            a.processCalculation()

        elif calctype == "EVI":
            entries.append(r1)
            entries.append(r2)
            entries.append(r3)
            expression = "2.5*(\"{0}\"-\"{1}\")/(\"{0}\"+6*\"{1}\"-7.5*\"{2}\"+1)".format(
                r1.ref, r2.ref, r3.ref)

            a = QgsRasterCalculator(expression, path, exporttype, rLayer1.extent(
            ), rLayer1.width(), rLayer1.height(), entries)

            a.processCalculation()

        else:
            self.com.error(Bold="CalcType Error",
                           String="Unrecognized calctype", level=2)
