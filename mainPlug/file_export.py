



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
        self.filePath = path
        self.ExportX = x
        self.ExportY = y
        self.XLLCorner = XCorner
        self.YLLCorner = YCorner
        self.cellSize = cellsize
        self.NoDataValue = NodataValue
        self.DataSet = DataSet

    def WriteFile(self):
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

