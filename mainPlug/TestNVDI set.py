import unittest

from file_export import FileExport
from rasterManip import RasterManip


class TestNVDI(unittest.TestCase):

    def setUp(self):
        self.TestSet1 = [{1: 10.1}, {1: 6}, {1: 7}]
        self.TestSet2 = [{1: 9}, {1: 10}, {1: 3}]
        self.RastManip = RasterManip(None)
        self.FileExport = FileExport()

    def tearDown(self):
        pass

    def testNDVI(self):
        a = self.RastManip.do_ndvi_calc(DataSet=self.TestSet1, DataSet2=self.TestSet2)
        print a
        self.FileExport.file_output("C:\Users\w0414043\Desktop\TestOutputs", 0, 0, 0, 0, 1, a)
        self.FileExport.WriteFile()
