# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mainPlug
                                 A QGIS plugin
 To allow Calculations to be done on raster layers
                             -------------------
        begin                : 2018-04-24
        copyright            : (C) 2018 by EAT Labs
        email                : foo@bar.com
        git sha              : $Format:%H$
 ***************************************************************************/

 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load mainPlug class from file mainPlug.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    from mainPlug import mainPlug
    import resources_rc
    resources_rc.qInitResources()
    return mainPlug(iface)
