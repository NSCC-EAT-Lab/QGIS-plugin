



class FileExport:

    def __init__(self):
        self.filePath = ''
        self.ExportX = 0
        self.ExportY = 0
        self.XLLCorner = 0
        self.YLLCorner = 0
        self.cellSize = 0
        self.NoDataValue = -9999
        self.DataSet = None

    def file_output(self, path, x, y, XCorner, YCorner, cellsize,DataSet, NodataValue=-9999 ):
        """
        Prep the file Output
        :param path: Path to the Output file
        :param x: Lenght of the Image
        :param y: Height of the image
        :param XCorner: Where X does it start (From the Bottom left corner)
        :param YCorner: Where does Y Start (From the bottom left corner)
        :param cellsize: What is the resolution of a single cell
        :param DataSet: The final compiled Dataset
        :param NodataValue: Default value if there is no data to fill a box
        :return: None
        """
        self.filePath = str(path)
        self.ExportX = x
        self.ExportY = y
        self.XLLCorner = XCorner
        self.YLLCorner = YCorner
        self.cellSize = cellsize
        self.NoDataValue = NodataValue
        self.DataSet = DataSet

    def WriteFile(self):
        """
        Write the ASCII TIFF raster file following documentation from http://resources.esri.com/help/9.3/ArcGISengine/java/Gp_ToolRef/Spatial_Analyst_Tools/esri_ascii_raster_format.htm
        :return:
        """

        OutData = ''

        for i in self.DataSet:
            OutData = OutData + str(i) + " "

        WriteString = "ncols {0}\n" \
                      "nrows {1}\n" \
                      "xllcorner {2}\n" \
                      "yllcorner {3}\n" \
                      "cellsize {4}\n" \
                      "nodata_value {5}\n" \
                      "{6}".format(self.ExportX, self.ExportY, self.XLLCorner, self.YLLCorner, self.cellSize, self.NoDataValue, OutData)
        if self.filePath != u'':
            f = open(self.filePath, 'w')
            f.write(WriteString)
            f.close()
        else:
            pass
