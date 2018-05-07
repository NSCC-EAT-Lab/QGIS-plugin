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
    os.path.dirname(__file__), 'ImportExport.ui'))


class ImportExportDialog(QtGui.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """
        Create a dialog for importing and exporting in the specific NDVI case
        :param parent: The window parent
        """
        """ TODO: Allow both input fields to allow any of the two image to end up in the correct spot (Likely using regex or something to determine what band the image falls under)"""
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
        self.FileSelect_4.clicked.connect(self.selectFile3)
        self.buttonBox.clicked.connect(self.ret_path)
        self.CalcBox.currentIndexChanged.connect(self.handle_Combobox)
        self.text = ''
        self.text2 = ''
        self.text3 = ''
        self.calc = ''
        self.exportText = ''

    def selectFile(self):
        """
        Open a file select dialog and set the path box to contain the file path
        :return:
        """
        self.FilePath.setText(QtGui.QFileDialog.getOpenFileName(self, "c:\\", "*.tif", "Any File(*.*);;Tiff (*.tif *.tiff);;"))

    def selectFile2(self):
        """
        Open the Second file, same as the selectFile
        :return:
        """
        # TODO: Compress this into one function
        self.FilePath_3.setText(QtGui.QFileDialog.getOpenFileName(self, "c:\\", "*.tif", "Any File(*.*);;Tiff (*.tif *.tiff);;"))

    def selectFile3(self):
        """
        Open Third File, Same as the selectFile
        :return:
        """
        self.FilePath_4.setText(QtGui.QFileDialog.getOpenFileName(self, "c:\\", "*.tif", "Any File(*.*);;Tiff (*.tif *.tiff);;"))

    def selectExport(self):
        """
        File path to export too, Similar to selectFile
        :return:
        """
        self.FilePath_2.setText(QtGui.QFileDialog.getSaveFileName(self, "c:\\", "*.tiff"))

    def ret_path(self):
        """
        Update values upon Dialog exit (Through OK)
        :return:
        """
        self.text = self.FilePath.text()
        self.text2 = self.FilePath_3.text()
        self.text3 = self.FilePath_4.text()
        self.calc = self.CalcBox.currentText()
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

    def get_text3(self):
        """
        Return Text from Textbox 3
        :return:
        """
        return self.text3

    def get_export(self):
        """
        Return Text from Export path box
        :return: ExportText -str
        """
        return self.exportText

    def get_calc(self):
        """
        Return the Calc Function being performed
        :return:
        """
        return self.calc

    def handle_Combobox(self):
        """
        Output User assistance text to Calc help corresponding to the calc type
        :return:
        """
        if self.CalcBox.currentText() == "NDVI":
            self.CalcHelp.setPlainText("NDVI is a calculation using Both the Near IR field and The visible Red Field\n"
                                       "To do this calculation the program requires either: Two Images, One In the Red Field (With the word \"Red\" in its name)"
                                       " And the other in the Near IR Field (With the word \"NIR\" In its name)\n"
                                       "Or One Image with Both NearIR and Red bands")
            self.FilePath_4.setEnabled(False)
            self.FileSelect_4.setEnabled(False)
        elif self.CalcBox.currentText() == "bNDVI":
            self.CalcHelp.setPlainText(
                "bNDVI is a calculation using Both the Near IR field and The visible Blue Field\n"
                "To do this calculation the program requires either: Two Images, One In the Blue Field (With the word \"Blue\" in its name)"
                " And the other in the Near IR Field (With the word \"NIR\" In its name)\n"
                "Or One Image with Both NearIR and Blue bands")
            self.FilePath_4.setEnabled(False)
            self.FileSelect_4.setEnabled(False)
        elif self.CalcBox.currentText() == "ENDVI":
            self.CalcHelp.setPlainText(
                "ENDVI (Enhanced NDVI) is a calculation in the Near IR Field, The Visible Green Field and the Visible Blue Field\n"
                "To do this calculation the program requires Either: One image with all Three Bands or \n"
                "Three images, each labeled with their respective bands (NIR, BLUE, GREEN")
            self.FilePath_4.setEnabled(True)
            self.FileSelect_4.setEnabled(True)
