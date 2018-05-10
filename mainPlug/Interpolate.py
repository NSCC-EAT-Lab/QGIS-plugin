
from processing.core.Processing import Processing
from processing.tools import *

class interp():
    def __init__(self, pointLayer):
        Processing.initialize()
        self.pLayer = pointLayer


    def run_Output(self):
        general.runalg('saga:simplekriging', self.pLayer)