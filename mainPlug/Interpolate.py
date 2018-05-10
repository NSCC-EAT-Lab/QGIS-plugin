
from processing.core.Processing import Processing
from processing.tools import *

from qgis.core import QgsPro

class interp():
    def __init__(self, pointLayer):
        Processing.initialize()
        self.pLayer = pointLayer


    def run_Output(self):

        """
        general.runalg('saga:simplekriging', iface.activeLayer(), "Sat_Mg", 1, 1, True,True,1, 1, 1, 1, "variance", 1000000, 1, 1, 10, 1, 0, 100, 1)

        ALGORITHM: Simple kriging
	POINTS <ParameterVector>
	FIELD <parameters from POINTS>
	TQUALITY <ParameterSelection>
	LOG <ParameterBoolean>
	BLOCK <ParameterBoolean>
	DBLOCK <ParameterNumber>
	VAR_MAXDIST <ParameterNumber>
	VAR_NCLASSES <ParameterNumber>
	VAR_NSKIP <ParameterNumber>
	VAR_MODEL <ParameterString>
	OUTPUT_EXTENT <ParameterExtent>
	TARGET_USER_SIZE <ParameterNumber>
	TARGET_USER_FITS <ParameterSelection>
	SEARCH_RANGE <ParameterSelection>
	SEARCH_RADIUS <ParameterNumber>
	SEARCH_POINTS_ALL <ParameterSelection>
	SEARCH_POINTS_MIN <ParameterNumber>
	SEARCH_POINTS_MAX <ParameterNumber>
	SEARCH_DIRECTION <ParameterSelection>
	PREDICTION <OutputRaster>
	VARIANCE <OutputRaster>


TQUALITY(Type of Quality Measure)
	0 - [0] standard deviation
	1 - [1] variance
TARGET_USER_FITS(Fit)
	0 - [0] nodes
	1 - [1] cells
SEARCH_RANGE(Search Range)
	0 - [0] local
	1 - [1] global
SEARCH_POINTS_ALL(Number of Points)
	0 - [0] maximum number of nearest points
	1 - [1] all points within search distance
SEARCH_DIRECTION(Search Direction)
	0 - [0] all directions
	1 - [1] quadrants
        :return:
        """

        # POINTS < ParameterVector >
        # FIELD < parameters
        # from POINTS >
        # TQUALITY < ParameterSelection >
        # LOG < ParameterBoolean >
        # BLOCK < ParameterBoolean >
        # DBLOCK < ParameterNumber >
        # VAR_MAXDIST < ParameterNumber >
        # VAR_NCLASSES < ParameterNumber >
        # VAR_NSKIP < ParameterNumber >
        # VAR_MODEL < ParameterString >
        # OUTPUT_EXTENT < ParameterExtent >
        # TARGET_USER_SIZE < ParameterNumber >
        # TARGET_USER_FITS < ParameterSelection >
        # SEARCH_RANGE < ParameterSelection >
        # SEARCH_RADIUS < ParameterNumber >
        # SEARCH_POINTS_ALL < ParameterSelection >
        # SEARCH_POINTS_MIN < ParameterNumber >
        # SEARCH_POINTS_MAX < ParameterNumber >
        # SEARCH_DIRECTION < ParameterSelection >
        # PREDICTION < OutputRaster >
        # VARIANCE < OutputRaster >


        # TESTING WITHIN THE PYTHON CONSOLE IN QGIS
        # general.runalg('saga:simplekriging', iface.activeLayer(), iface.activeLayer().name(), 0, False, False, 1, -1, 100, 1, "a + b * x", iface.activeLayer().extent(), 0.000001, 1, 0, 0, 1000, 1, 4, 20, 0, "tmp1.sdat", "tmp2.sdat")
        general.runalg('saga:simplekriging', self.pLayer, self.pLayer.baseName, 0, False, False, 1, -1, 100, 1, "a + b * x", self.pLayer.extent(), 0.000001, 1, 0, 0, 1000, 1, 4, 20, 0, "tmp1.sdat", "tmp2.sdat")