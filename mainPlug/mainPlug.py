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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, pyqtSignal
from PyQt4.QtGui import QAction, QIcon
#from PyQt4.QtWidgets import QAction

# Initialize Qt resources from file resources.py
# import resources
# Import the code for the dialog
from mainPlug_dialog import mainPlugDialog
from file_input_dialog import FileInputDialog
from aboutDialog import AboutDialog
from file_Import import FileImport
from rasterManip import RasterManip
from importexport_dialog import ImportExportDialog

from qgis.core import QgsPoint, QgsRaster
import os.path


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
        self.menu = self.tr(u'&DeadBeef')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'mainPlug')
        self.toolbar.setObjectName(u'mainPlug')
        self.DialogStore = [None]*15

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
        self.add_action(
            icon_path,
            store_val=0,
            text=self.tr(u'PlotData'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.add_action(
            icon_path,
            store_val=1,
            text=self.tr(u'File_Import_Test'),
            callback=self.run_file_input,
            dialog=FileInputDialog()
        )
        self.add_action(
            about_path,
            store_val=2,
            text=self.tr(u'About'),
            callback=self.runabout,
            dialog=AboutDialog()
        )
        self.add_action(
            icon_path,
            store_val=3,
            text=self.tr(u'Calculate NDVI'),
            callback=self.run_calc_ndvi,
            dialog=ImportExportDialog()
        )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&DeadBeef'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

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

        if result:
            resul = diag.get_text()
            print("Result: ")
            print(resul)
            fIO.file_input(resul)
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
        Run the NDVI Calculation and return it
        :return:
        """

        fIO = FileImport()
        fIO2 = FileImport()

        diag = self.DialogStore[3]
        diag.show()

        result = diag.exec_()

        DataSet = []
        DataSet2 = []

        if result:
            resul = diag.get_text()
            resul2 = diag.get_text2()

            fIO.file_input(resul)
            self.iface.addRasterLayer(fIO.filePath, fIO.baseName)
            if resul2 != '':
                fIO2.file_input(resul2)
                self.iface.addRasterLayer(fIO2.filePath, fIO.baseName)

                rLayerX = fIO.rLayer.width()
                rLayerY = fIO.rLayer.height()

                a = RasterManip(iface=self.iface)

                for i in range(rLayerY):
                    for j in range(rLayerX):

                        p = a.return_dataset(i, -j, rLayer=fIO.rLayer)
                        g = a.return_dataset(i, -j, rLayer=fIO2.rLayer)
                        print p
                        print g
                        print i
                        print j
                        DataSet.append(p)
                        DataSet2.append(g)

            else:
                rLayerX = fIO.rLayer.width()
                rLayerY = fIO.rLayer.height()
                a = RasterManip(iface=self.iface)

                for i in range(rLayerX):
                    for j in range(rLayerY):
                        print i
                        print j
                        p = a.return_dataset(i, -j, rLayer=fIO.rLayer)
                        print p
                        DataSet.append(p)
            c = ''
            for i in DataSet:
                c = c + " " + str(i.get(1))
                print c





    def runabout(self):
        self.DialogStore[2].show()
