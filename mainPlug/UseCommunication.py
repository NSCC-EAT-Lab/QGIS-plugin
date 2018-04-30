from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar

class Communicate():

    def __init__(self, iface):
        self.iface = iface

    def log(self, String, level):
        """
        Log a Message
        :param String: Message you wish to log
        :param level: Message Importance (0-2 | 0=Info | 1=Warning | 2=Critical)
        :return: None
        """
        lvl = None
        if level == 0:
            lvl = QgsMessageLog.INFO
        elif level == 1:
            lvl = QgsMessageLog.WARNING
        elif level == 2:
            lvl = QgsMessageLog.CRITICAL

        QgsMessageLog.logMessage(String, "DeadBeef", level=lvl)

    def error(self, String, level, Bold=None, duration=None):
        if Bold is not None:
            bld = Bold
        else:
            bld = None

        lvl=None
        if level == 0:
            lvl = QgsMessageBar.INFO
            if bld is None:
                bld = "INFO"
        elif level == 1:
            lvl = QgsMessageBar.WARNING
            if bld is None:
                bld = "WARNING"
        elif level == 2:
            lvl = QgsMessageBar.CRITICAL
            if bld is None:
                bld = "CRITICAL"

        self.iface.messageBar().pushMessage(bld, String, level=lvl, duration=duration)