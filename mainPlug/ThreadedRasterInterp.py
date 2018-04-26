
from RasterInterpObj import InterpObj

class ThreadDataInterp:

    def __init__(self, iface, rLayer):
        """
        Process one Raster, returning the Dataset
        :param iface:
        :param rLayer:
        """
        self.iface = iface
        self.rLayer = rLayer

        self.FinishedDataset = []
        self.FinishOrder = []
        self.DataStore = []

        self.rLayerX = rLayer.width()
        self.rLayerY = rLayer.height()
        self.ThreadArray = []

    def InitThreads(self):
        v = 0
        for i in range(self.rLayerY):
            self.ThreadArray.append(InterpObj(iface=self.iface, rLayer=self.rLayer, DataStore=self.DataStore,
                                              Finishorder=self.FinishOrder, Yval=i))
            v += 1

        for i in self.ThreadArray:
            i.start()

        for i in self.ThreadArray:
            i.join()

        a = 0
        while a != v:

            for i in self.ThreadArray:
                if i.isAlive() is False:
                    a += 1
        self.ConvertToFinish()

    def ConvertToFinish(self):
        pass