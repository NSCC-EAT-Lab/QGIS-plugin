from RasterInterpObj import InterpObj
from threading import Thread
from UseCommunication import Communicate


class ThreadDataInterp(Thread):

    def __init__(self, iface, rLayer):
        """
        Process one Raster, returning the Dataset
        :param iface: QGIS Iface
        :param rLayer: rLayer object to Process
        """
        Thread.__init__(self)

        self.iface = iface
        self.rLayer = rLayer
        self.com = Communicate(self.iface)
        self.FinishedDataset = []
        self.FinishOrder = []
        self.DataStore = []

        self.rLayerX = rLayer.width()
        self.rLayerY = rLayer.height()
        self.ThreadArray = []

    def ProcessrLayer(self):
        """
        Setup a thread for each Y Value in rLayer
        TODO: Test to see if doing a thread per pixel would Speed things up or if Near Approximation would help
        :return: The final Stitched Dataset of rLayer (After being passed to ConvertToFinish)
        """
        self.com.log("Producing Threads for Interpretation", 0)
        v = 0
        for i in range(self.rLayerY):
            self.ThreadArray.append(InterpObj(iface=self.iface, rLayer=self.rLayer, DataStore=self.DataStore,
                                              Finishorder=self.FinishOrder, Yval=i))
            v += 1

        for i in self.ThreadArray:
            i.start()

        for i in self.ThreadArray:
            i.join(5)

        self.com.log("Threaded Interp Finished", 0)
        return self.ConvertToFinish()

    def ConvertToFinish(self):
        """
        Restitch the Jumbled Dataset (Due to Concurrent Returns)
        :return: The ReStitched DataSet
        """
        for idx, val in enumerate(self.FinishOrder):
            # print str(idx), str(val)
            for i in self.DataStore[idx]:
                self.FinishedDataset.append(i)
        return self.FinishedDataset

    def run(self):
        return self.ProcessrLayer()
