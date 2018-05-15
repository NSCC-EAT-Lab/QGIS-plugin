from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsPoint, QgsRaster

rasterobject = None

# A list of QgsRasterCalculatorEntries, We append to this for later inputs
entries = []

path = "Path to export"

# Replace this with your raster object likely taken in from FileInput
raster = rasterobject

# Initilize the Raster Calculator Entries
rasterEntry1 = QgsRasterCalculatorEntry()
rasterEntry2 = QgsRasterCalculatorEntry()

# start assigning names for these things
rasterEntry1.ref = "raster1"
rasterEntry2.ref = "raster2"

rasterEntry1.bandNumber = 1  # This is the band to work from
rasterEntry2.bandNumber = 1

rasterEntry1.raster = raster

entries.append(rasterEntry1)

expression = "(\"{0}\"-\"{1}\")/(\"{2}\"+\"{3}\")".format(rasterEntry1.ref,
                                                          rasterEntry2.ref, rasterEntry1.ref, rasterEntry2.ref)

# This follows the following requirements, the expression, path too, Export type, the extend of the image, the width then height followed by the rastercalc entries
a = QgsRasterCalculator(expression, path, 'GTiff', raster.extent(
), raster.width(), raster.height(), entries)
