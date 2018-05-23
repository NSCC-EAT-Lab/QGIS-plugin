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
"""
import os.path
import re

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QColor
from qgis.core import QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer, QgsRasterBandStats, \
    QgsRasterFileWriter, QgsRasterPipe

from CsvImport_Dialog import CsvInputdialog
from UseCommunication import Communicate
from aboutDialog import AboutDialog
from file_Import import FileImport
from help_dialog import HelpDialog
from importexport_dialog import ImportExportDialog
from krig_dialog import KrigDialog
# Initialize Qt resources from file resources.py
# import resources
# Import the code for the dialog
from mainPlug_dialog import mainPlugDialog
from rasterManip import RasterManip


# from PyQt4.QtWidgets import QAction


class mainPlug:
    """QGIS Plugin main body Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # type: object
        # Save reference to the QGIS interface
        self.output_set = None
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

        # Do some C like shenanigans
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
        # type: (object, object, object, object, object, object, object,object, object, object, object) -> object
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

        # noinspection PyTypeChecker
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
        self.com.log("Add_Action: Calculate NDVI", 0)

        self.add_action(
            icon_path,
            store_val=5,
            text=self.tr(u'Plot Soil data'),
            callback=self.run_SoilSample,
            dialog=CsvInputdialog()
        )

        self.add_action(
            icon_path,
            store_val=4,
            text=self.tr(u'Help'),
            callback=self.run_help,
            dialog=HelpDialog()
        )

        self.add_action(
            icon_path,
            store_val=6,
            text=self.tr(u'Krig'),
            callback=self.run_krig,
            dialog=KrigDialog()
        )

    def unload(self):
        """
        Removes the plugin menu item and icon from QGIS GUI.
        """
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&EggAGGIS'),
                action)
            self.iface.removeToolBarIcon(action)

        # remove the toolbar
        del self.toolbar
        self.com.log("Unload Toolbar: Success", 0)

    def run(self):
        """
        Run method that performs all the real work
        """
        # show the dialog
        self.DialogStore[0].show()
        # Run the dialog event loop
        result = self.DialogStore[0].exec_()
        # See if OK was pressed

        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def run_SoilSample(self):
        """
        Run the CSV input dialog for Soil Sample input
        :return:
        """
        from DataParse import IOParse
        diag = self.DialogStore[5]

        diag.show()

        result = diag.exec_()

        if result:
            result = diag.get_text()

            io_parse_result = IOParse(result, self.iface)
            io_parse_result.ReadFile()

    def run_file_input(self):
        """
        Run file input
        :return:
        """
        file_input = FileImport()
        diag = self.DialogStore[1]
        diag.show()
        result = diag.exec_()
        self.com.log("File Input Called", 0)

        if result:
            diag_result = diag.get_text()
            print("Result: ")
            print(diag_result)
            file_input.file_input(diag_result)
            self.com.log("File Input Result: {0} | {1}".format(
                file_input.filePath, file_input.baseName), 0)
            self.iface.addRasterLayer(file_input.filePath, file_input.baseName)

            print(file_input.rLayer.renderer().type())
            r_layer_x = file_input.rLayer.width()
            r_layer_y = file_input.rLayer.height()
            raster_manipulator = RasterManip(file_input.rLayer, self.iface)
            for i in range(r_layer_x):
                for j in range(r_layer_y):
                    print i
                    print j
                    raster_manipulator.return_dataset(i, -j)

    # noinspection PyBroadException
    def run_calc_ndvi(self):

        #         Warning to any maintainers, This is super spaghetti... I'm sorry, may the lord have mercy on your soul
        #         If you don't want things to explode, the horses don't go
        #         This is the best possible solution beyond doing if elif loops which would have been impossible
        #          to maintain
        #         If ye must pass I'll explain the best I can:
        """
        Handle the NDVI Calc Window Sending the values to where they're needed and Exporting the final result to disk

        This entire bit is to determine the files inputted and their respective bands, be they NIR, RED, BLUE or GREEN
        Using the names of the files, Clever List usage and some Regex, We pass the rLayers (Raster Layer objects) in
        the correct order for the actual NDVI calculation in rasterManip, taking into account the Calculation type that
        the user has given



        :return: None
        :rtype: None
        """

        nir_pattern = re.compile(r"NIR", re.IGNORECASE)
        red_pattern = re.compile(r"RED", re.IGNORECASE)
        blue_pattern = re.compile(r"BLUE", re.IGNORECASE)
        green_pattern = re.compile(r"GREEN", re.IGNORECASE)

        file_input_1 = FileImport()
        file_input_2 = FileImport()
        file_input_3 = FileImport()

        file_in_4 = FileImport()
        diag = self.DialogStore[3]
        diag.show()

        sort = [None, None, None]
        result = diag.exec_()

        raster_manipulator = RasterManip(iface=self.iface)
        if result:
            result = diag.get_text()
            result2 = diag.get_text2()
            result3 = diag.get_text3()

            file_input_1.file_input(result)
            self.com.log("File Input Result {0} | {1}".format(
                file_input_1.filePath, file_input_1.baseName), 0)
            if result2 != '':
                file_input_2.file_input(result2)
                self.com.log("File Input Result {0} | {1}".format(
                    file_input_2.filePath, file_input_2.baseName), 0)

                if diag.get_calc() == "ENVDI" or diag.get_calc() == "EVI":
                    if result3 != '':
                        file_input_3.file_input(result3)
                        self.com.log("File Input Result {0} | {1}".format(file_input_3.filePath, file_input_3.baseName),
                                     0)

                        # Sort the Rasters based on name into their correct
                        # positions
                        sort_old = [file_input_1, file_input_2, file_input_3]
                        for i in sort_old:
                            if nir_pattern.search(i.baseName) is not None:
                                self.com.log(str(sort), level=0)
                                sort[0] = i
                                self.com.log(str(sort), level=0)

                            if green_pattern.search(i.baseName) is not None:
                                self.com.log(str(sort), level=0)
                                sort[1] = i
                                self.com.log(str(sort), level=0)

                            if blue_pattern.search(i.baseName) is not None:
                                self.com.log(str(sort), level=0)
                                sort[2] = i
                                self.com.log(str(sort), level=0)

                        if len(sort) != 3:
                            self.com.error(
                                String="One of the Files is not labeled correctly, "
                                       "please Fix this and Rerun the program",
                                level=2)
                            return 0

                        else:
                            if diag.get_calc() == "ENDVI":
                                raster_manipulator.rastercalcmulti_ndvi(rLayer1=sort[0].rLayer, rLayer2=sort[1].rLayer,
                                                                        rLayer3=sort[2].rLayer,
                                                                        path=diag.exportText, calctype="ENVDI")
                            elif diag.get_calc() == "EVI":
                                raster_manipulator.rastercalcmulti_ndvi(rLayer1=sort[0].rLayer, rLayer2=sort[1].rLayer,
                                                                        rLayer3=sort[2].rLayer,
                                                                        path=diag.exportText, calctype="EVI")
                else:
                    if diag.get_calc() == "NDVI":

                        sort_old = [file_input_1, file_input_2]
                        for i in sort_old:
                            if nir_pattern.search(i.baseName) is not None:
                                self.com.log(str(sort), level=0)
                                sort[0] = i
                                self.com.log(str(sort), level=0)

                            if red_pattern.search(i.baseName) is not None:
                                self.com.log(str(sort), level=0)
                                sort[1] = i
                                self.com.log(str(sort), level=0)

                        if len(sort) != 3:
                            self.com.error(
                                String="One of the Files is not labeled correctly,"
                                       " please Fix this and Rerun the program",
                                level=2)
                            return 0
                        else:
                            raster_manipulator.rastercalcmulti_ndvi(rLayer1=sort[0].rLayer, rLayer2=sort[1].rLayer,
                                                                    path=diag.exportText,
                                                                    calctype="NDVI")

                    elif diag.get_calc() == "bNDVI":
                        sort_old = [file_input_1, file_input_2]
                        for i in sort_old:
                            if nir_pattern.search(i.baseName) is not None:
                                self.com.log(str(sort), level=0)
                                sort[0] = i
                                self.com.log(str(sort), level=0)

                            if blue_pattern.search(i.baseName) is not None:
                                self.com.log(str(sort), level=0)
                                sort[1] = i
                                self.com.log(str(sort), level=0)

                        if len(sort) != 3:
                            self.com.error(
                                String="One of the Files is not labeled correctly,"
                                       " please Fix this and Rerun the program",
                                level=2)
                            return 0
                        else:
                            raster_manipulator.rastercalcmulti_ndvi(rLayer1=sort[0].rLayer, rLayer2=sort[1].rLayer,
                                                                    path=diag.exportText,
                                                                    calctype="bNDVI")

            # THIS IS FAILOVER For Single raster input
            else:
                if diag.get_calc() == "ENDVI":
                    try:
                        raster_manipulator.rastercalcmulti_ndvi(calctype="ENDVI", rLayer1=file_input_1.rLayer,
                                                                rLayer2=file_input_1.rLayer,
                                                                rLayer3=file_input_1.rLayer, r1Band=1, r2Band=2,
                                                                r3Band=3, path=diag.exportText)
                    except BaseException:
                        self.com.error(
                            String="An Error Occurred upon Execution, Verify that the Input files are correct", level=2)
                elif diag.get_calc() == "bNDVI":
                    try:
                        raster_manipulator.rastercalcmulti_ndvi(calctype="bNDVI", rLayer1=file_input_1.rLayer,
                                                                rLayer2=file_input_1.rLayer, r1Band=1,
                                                                r2Band=2, path=diag.exportText)

                    except BaseException:
                        self.com.error(
                            String="An Error Occurred upon Execution, Verify that the Input files are correct", level=2)

                elif diag.get_calc() == "NDVI":
                    try:
                        raster_manipulator.rastercalcmulti_ndvi(calctype="NDVI", rLayer1=file_input_1.rLayer,
                                                                rLayer2=file_input_1.rLayer, r1Band=1,
                                                                r2Band=2, path=diag.exportText)
                    except BaseException:
                        self.com.error(
                            String="An Error Occurred upon Execution, Verify that the Input files are correct", level=2)

                elif diag.get_calc() == "EVI":
                    try:
                        raster_manipulator.rastercalcmulti_ndvi(calctype="EVI", path=diag.exportText,
                                                                rLayer1=file_input_1.rLayer,
                                                                rLayer2=file_input_1.rLayer,
                                                                rLayer3=file_input_1.rLayer, r1Band=1, r2Band=2,
                                                                r3Band=3)
                    except BaseException:
                        self.com.error(
                            String="An Error Occurred upon Execution, Verify that the Input files are correct", level=2)

            file_in_4.file_input(diag.exportText)
            self.Color(file_in_4, calcType=diag.get_calc())
        else:
            self.com.error(String="NO RESULT", level=2)

    def Color(self, file_in, calcType=None):
        """
        Color the Inbound file (Essentially the File we JUST exported) and display it to screen)

        :param file_in: The file that was just exported
        :type file_in: FileImport

        :return: TO SCREEN Rendered Image
        :rtype: None
        """
        k = self.iface.addRasterLayer(file_in.filePath, file_in.baseName)
        stats = k.dataProvider().bandStatistics(
            1, QgsRasterBandStats.All, k.extent(), 0)
        minimum = stats.minimumValue
        maximum = stats.maximumValue

        self.com.log("Color func: [Min val: {0} | Max val: {1}".format(
            str(minimum), str(maximum)), level=0)

        ramp_shader = QgsColorRampShader()
        ramp_shader.setColorRampType(QgsColorRampShader.INTERPOLATED)

        if calcType is None:
            color_list = [QgsColorRampShader.ColorRampItem(minimum, QColor(255, 0, 0)),
                          QgsColorRampShader.ColorRampItem(
                              0, QColor(255, 207, 74, 255)),
                          QgsColorRampShader.ColorRampItem(maximum, QColor(0, 255, 0))]

        elif calcType == "EVI":
            color_list = [QgsColorRampShader.ColorRampItem(-2, QColor(255, 0, 0)),
                          QgsColorRampShader.ColorRampItem(
                              0, QColor(255, 207, 74, 255)),
                          QgsColorRampShader.ColorRampItem(2, QColor(0, 255, 0))]

        else:
            color_list = [QgsColorRampShader.ColorRampItem(minimum, QColor(255, 0, 0)),
                          QgsColorRampShader.ColorRampItem(
                              0, QColor(255, 207, 74, 255)),
                          QgsColorRampShader.ColorRampItem(maximum, QColor(0, 255, 0))]

        ramp_shader.setColorRampItemList(color_list)

        shader = QgsRasterShader()
        shader.setRasterShaderFunction(ramp_shader)

        renderer = QgsSingleBandPseudoColorRenderer(
            k.dataProvider(), 1, shader)
        k.setRenderer(renderer)

        """
        Export colored image to file
        """
        export_path = file_in.filePath + ".colored.tif"
        file_writer = QgsRasterFileWriter(export_path)
        pipe = QgsRasterPipe()
        provide = k.dataProvider()

        # Pipe Setter
        if not pipe.set(provide.clone()):
            self.com.error(Bold="PipeProviderError:",
                           String="Cannot set pipe provider", level=1, duration=3)
            self.com.log(
                "mainPlug - Color: Pipe provider error on line 473, Continuing...", level=1)

        self.com.log(str(pipe.renderer()), level=0)
        pipe.set(renderer.clone())
        file_writer.writeRaster(pipe, provide.xSize(
        ), provide.ySize(), provide.extent(), provide.crs())

    def run_krig(self):
        """
        Create and run the Krig Window and spoole off the Kriging process for all Layers
        TODO: Implement a Per layer toggle vs the current only mass layer
        :return: None
        """
        diag = self.DialogStore[6]

        from Interpolate import interp

        diag.show()

        result = diag.exec_()

        if result:
            map_layers = self.iface.mapCanvas().layers()
            if diag.retProcessallState():
                for Index, value in enumerate(
                        map_layers):  # type: (int, object)

                    a = interp(iface=self.iface, pointLayer=value)
                    a.run_Output()

    def run_help(self):
        """
        Display Help Dialog
        :return:
        """
        self.DialogStore[4].show()

    def runabout(self):
        """
        Display the About page
        :return:
        """
        self.DialogStore[2].show()
