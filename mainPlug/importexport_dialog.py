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

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import QObject, pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ImportExport.ui'))


class ImportExportDialog(QtGui.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(ImportExportDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.FileSelect.clicked.connect(self.selectFile)
        self.FileSelect_3.clicked.connect(self.selectFile2)
        self.FileSelect_2.clicked.connect(self.selectExport)
        self.buttonBox.clicked.connect(self.ret_path)
        self.text = ''
        self.text2 = ''
        self.exportText = ''


    def selectFile(self):
        """
        Open a file select dialog and set the path box to contain the file path
        :return:
        """
        self.FilePath.setText(QtGui.QFileDialog.getOpenFileName())

    def selectFile2(self):
        """
        Open the Second file, same as the selectFile
        :return:
        """
        # TODO: Compress this into one function
        self.FilePath_3.setText(QtGui.QFileDialog.getOpenFileName())

    def selectExport(self):
        self.FilePath_2.setText(QtGui.QFileDialog.getSaveFileName())

    def ret_path(self):
        self.text = self.FilePath.text()
        self.text2 = self.FilePath_3.text()
        self.exportText = self.FilePath_2.text()

    def get_text(self):
        """
        Get text from textbox 1
        :return: Text - Str
        """
        return self.text

    def get_text2(self):
        """
        Get Text From textbox 2
        :return: Text2 - str
        """
        return self.text2

    def get_export(self):
        return self.exportText
