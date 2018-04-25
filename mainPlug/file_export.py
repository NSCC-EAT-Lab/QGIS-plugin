



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
        self.filePath = path
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
        WriteString = "ncols {0}" \
                      "nrows {1}" \
                      "xllcorner {2}" \
                      "yllcorner {3}" \
                      "cellsize {4}" \
                      "nodata_value {5}" \
                      "{6}".format(self.ExportX, self.ExportY, self.XLLCorner, self.YLLCorner, self.cellSize, self.NoDataValue, str(self.DataSet))
        f = open(self.filePath, 'w')
        f.write(WriteString)
        f.close()

