# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mainPlug
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
import os.path
import re

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QColor
from qgis.core import QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer

from qgis.core import QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer, QgsMapLayerRegistry
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer
from ThreadedRasterInterp import ThreadDataInterp
from UseCommunication import Communicate
from aboutDialog import AboutDialog
from file_Import import FileImport
from file_export import FileExport
from help_dialog import HelpDialog
from importexport_dialog import ImportExportDialog
# Initialize Qt resources from file resources.py
# import resources
# Import the code for the dialog
from mainPlug_dialog import mainPlugDialog
from rasterManip import RasterManip


# from PyQt4.QtWidgets import QAction


class mainPlug:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        self.com = Communicate(self.iface)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'mainPlug_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&EggAGGIS')
        self.toolbar = self.iface.addToolBar(u'mainPlug')
        self.toolbar.setObjectName(u'mainPlug')
        self.DialogStore = [None] * 15

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('mainPlug', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            store_val,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None,
            dialog=mainPlugDialog()):

        """Add a toolbar icon to the toolbar.

        :param store_val: This value is the position to store the Dialog within the dialog list, Note that this position
        can and will interfere with standard operation if it is stored in an incorrect position at this time
        :type store_val: int

        :param dialog: The dialog you wish to Display to users
        :type dialog: function

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.DialogStore[store_val] = dialog

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/mainPlug\icon.png'
        about_path = ':/plugins/mainPlug\\about.png'
        """self.add_action(
            icon_path,
            store_val=0,
            text=self.tr(u'PlotData'),
            callback=self.run,
            parent=self.iface.mainWindow())"""

        """self.add_action(
            icon_path,
            store_val=1,
            text=self.tr(u'File_Import_Test'),
            callback=self.run_file_input,
            dialog=FileInputDialog()
        )"""
        self.add_action(
            about_path,
            store_val=2,
            text=self.tr(u'About'),
            callback=self.runabout,
            dialog=AboutDialog()
        )
        self.com.log("Add_action: About", 0)
        self.add_action(
            icon_path,
            store_val=3,
            text=self.tr(u'Calculate NDVI'),
            callback=self.run_calc_ndvi,
            dialog=ImportExportDialog()
        )
        self.add_action(
            icon_path,
            store_val=4,
            text=self.tr(u'Help'),
            callback=self.run_help,
            dialog=HelpDialog()
        )
        self.com.log("Add_Action: Calculate NDVI", 0)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&DeadBeef'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        self.com.log("Unload Toolbar: Success", 0)

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.DialogStore[0].show()
        # Run the dialog event loop
        result = self.DialogStore[0].exec_()
        # See if OK was pressed

        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def run_file_input(self):
        """
        Run file input
        :return:
        """
        fIO = FileImport()
        diag = self.DialogStore[1]
        diag.show()
        result = diag.exec_()
        self.com.log("File Input Called", 0)

        if result:
            resul = diag.get_text()
            print("Result: ")
            print(resul)
            fIO.file_input(resul)
            self.com.log("File Input Result: {0} | {1}".format(fIO.filePath, fIO.baseName), 0)
            self.iface.addRasterLayer(fIO.filePath, fIO.baseName)

            print(fIO.rLayer.renderer().type())
            rLayerX = fIO.rLayer.width()
            rLayerY = fIO.rLayer.height()
            a = RasterManip(fIO.rLayer, self.iface)
            for i in range(rLayerX):
                for j in range(rLayerY):
                    print i
                    print j
                    a.return_dataset(i, -j)

    def run_calc_ndvi(self):
        """
        Handle the NDVI Calc Window Sending the values to where they're needed and Exporting the final result to disk
        :return:
        """

        NIRpattern = re.compile(r"NIR", re.IGNORECASE)
        REDpattern = re.compile(r"RED", re.IGNORECASE)

        fIO = FileImport()
        fIO2 = FileImport()

        fOut = FileExport()

        fileIn = FileImport()
        diag = self.DialogStore[3]
        diag.show()

        result = diag.exec_()

        a = RasterManip(iface=self.iface)
        self.outputSet = None
        if result:
            result = diag.get_text()
            result2 = diag.get_text2()

            fIO.file_input(result)
            self.com.log("File Input Result {0} | {1}".format(fIO.filePath, fIO.baseName), 0)
            # self.iface.addRasterLayer(fIO.filePath, fIO.baseName)

            if result2 != '':
                self.com.log("Input contains 2 Inputs, Doing Raster Calculator", 0)
                fIO2.file_input(result2)

                if NIRpattern.search(fIO.baseName) is not None:
                    if REDpattern.search(fIO2.baseName) is not None:
                        a.Processing_ndvi_calc(fIO.rLayer, fIO2.rLayer, diag.exportText)
                elif REDpattern.search(fIO.baseName) is not None:
                    if NIRpattern.search(fIO2.baseName) is not None:
                        a.Processing_ndvi_calc(fIO2.rLayer, fIO.rLayer, diag.exportText)
                else:
                    self.com.log("Double Pattern set Mismatch", level=0)
                    self.com.error(Bold="File Name Error:",
                                   String="Please label the files NIR and RED respectively (See help for Details)",
                                   level=2)
            else:
                q = ThreadDataInterp(iface=self.iface, rLayer=fIO.rLayer)
                rec = q.ProcessrLayer()
                self.outputSet = a.do_ndvi_calc(DataSet=rec)
            # print diag.exportText
            
            fileIn.file_input(diag.exportText)
            k = self.iface.addRasterLayer(fileIn.filePath, fIO.baseName)

            # TODO: Put this in a separate class
            fcn = QgsColorRampShader()
            fcn.setColorRampType(QgsColorRampShader.INTERPOLATED)
            color_list = [QgsColorRampShader.ColorRampItem(-1, QColor(255, 0, 0)),
                          QgsColorRampShader.ColorRampItem(1, QColor(0, 255, 0))]
            fcn.setColorRampItemList(color_list)

            shader = QgsRasterShader()
            shader.setRasterShaderFunction(fcn)

            renderer = QgsSingleBandPseudoColorRenderer(k.dataProvider(), 1, shader)
            k.setRenderer(renderer)


    def run_help(self):
        self.DialogStore[4].show()

    def runabout(self):
        self.DialogStore[2].show()
