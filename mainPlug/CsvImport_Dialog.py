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
    os.path.dirname(__file__), 'CsvImport.ui'))


# noinspection PyCallByClass
class CsvInputdialog(QtGui.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(CsvInputdialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.FileSelect.clicked.connect(self.selectFile)
        self.buttonBox.clicked.connect(self.ret_path)
        self.text = ''
        self.text2 = ''

    def selectFile(self):
        """
        Open a file select dialog and set the path box to contain the file path
        :return:
        """
        self.FilePath.setText(QtGui.QFileDialog.getOpenFileName(
            self, "c:\\", "*.txt", "Text files (.txt)"))

    def ret_path(self):
        """
        Update values upon Dialog exit (Through OK)
        :return:
        """
        self.text = self.FilePath.text()

    def get_text(self):
        """
        Get text from textbox 1
        :return: Text - Str
        """
        return self.text
