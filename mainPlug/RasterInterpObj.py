
from threading import Thread
from rasterManip import RasterManip

class InterpObj(Thread):

    def __init__(self, iface, rLayer, DataStore, Finishorder, Yval):

        Thread.__init__(self)
        self.iface = iface
        self.rLayer = rLayer
        self.DataStore = DataStore
        self.Finishorder = Finishorder
        self.Yval = Yval
        self.a = RasterManip(iface=self.iface)

        self.internalData = []

    def run(self):
        for i in range(self.rLayer.width()):
            ret = self.a.return_dataset(i, -self.Yval, rLayer=self.rLayer)

            self.internalData.append(ret)

        self.DataStore.append(self.internalData)
        self.Finishorder.append(self.Yval)
