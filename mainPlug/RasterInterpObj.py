
from threading import Thread
from rasterManip import RasterManip

class InterpObj(Thread):

    def __init__(self, iface, rLayer, DataStore, Finishorder, Yval):
        """
        Interpret a row of the rLayer given based off the given Y-Value.

        :param iface: QGis Iface
        :param rLayer: rLayer Pointer
        :param DataStore: DataStore Pointer
        :param Finishorder: Finish Order Array pointer
        :param Yval: The Y row
        """

        Thread.__init__(self)
        self.iface = iface
        self.rLayer = rLayer
        self.DataStore = DataStore
        self.Finishorder = Finishorder
        self.Yval = Yval
        self.a = RasterManip(iface=self.iface)

        self.internalData = []

    def run(self):
        """
        Grab the value of Every X pixel in the Y row on the Given rLayer

        :return: Appending The Value to a new Array within the Datastore array and The given Y value to the Finish order
        signaling it's time of completion
        """
        for i in range(self.rLayer.width()):
            ret = self.a.return_dataset(i, -self.Yval, rLayer=self.rLayer)

            self.internalData.append(ret)

        self.DataStore.append(self.internalData)
        self.Finishorder.append(self.Yval)
