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
    os.path.dirname(__file__), 'File_Select.ui'))


class FileInputDialog(QtGui.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """
        This is a Test File Input dialog, Mostly used as a Template and for testing user input
        :param parent: the parent to this dialog
        """
        super(FileInputDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.FileSelector.clicked.connect(self.selectFile)
        self.buttonBox.clicked.connect(self.ret_path)
        self.text = ''
        self.text2 = ''

    def selectFile(self):
        self.FilePath.setText(QtGui.QFileDialog.getOpenFileName())

    def ret_path(self):
        self.text = self.FilePath.text()

    def get_text(self):
        return self.text
