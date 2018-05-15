"""
This Entire Scratch is for use within QGIS's Internal Python interpereter

This will generate a Krig based on the currently selected layer
"""


from processing.core.Processing import processing
from processing.tools import *

alg = 'saga:simplekriging'

layer = iface.activeLayer()
ext = layer.extent()

xmin = ext.xMinimum()
xmax = ext.xMaximum()
ymin = ext.yMinimum()
ymax = ext.yMaximum()

coords = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)

params = {"POINTS": iface.activeLayer(), "FIELD": iface.activeLayer().name(), "TQUALITY": 0, "LOG": False, "BLOCK": False,
          "DBLOCK": 1, "VAR_MAXDIST": -1, "VAR_NCLASSES": 100, "VAR_NSKIP": 1, "VAR_MODEL": "a+b*x",
          "OUTPUT_EXTENT": coords, "TARGET_USER_SIZE": 0.000001, "TARGET_USER_FITS": 0,
          "SEARCH_RANGE": 0, "SEARCH_RADIUS": 1000, "SEARCH_POINTS_ALL": 0, "SEARCH_POINTS_MIN": 4, "SEARCH_POINTS_MAX": 20, "SEARCH_DIRECTION": 0}

# params = {"POINTS": iface.activeLayer(), "FIELD": iface.activeLayer().name(), "TQUALITY": 0, "LOG": False, "BLOCK": False,
#            "DBLOCK": 1, "TARGET_USER_SIZE": 0.000001}


processing.runalg(alg, params)
