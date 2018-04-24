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

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
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
    return mainPlug(iface)
