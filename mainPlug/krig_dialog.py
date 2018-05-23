# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mainPlugDialog
                                 A QGIS plugin
 To allow Calculations to be done on raster layers
                             -------------------
        begin                : 2018-04-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by EAT Labs
        email                : foo@bar.com
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'KrigDialog.ui'))


class KrigDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Create the Krig Dialog box
        :param parent:
        """
        super(KrigDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.buttonBox.clicked.connect(self.retval)
        self.processall = False

    def retval(self):
        self.processall = self.Processall.isChecked()


    def retProcessallState(self):
        """
        Return if processall is Checked
        :return: processall state
        :rtype: bool
        """
        return self.processall
