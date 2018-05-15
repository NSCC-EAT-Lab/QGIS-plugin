from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar


class Communicate():

    def __init__(self, iface=None):
        self.iface = iface

    def log(self, String, level):
        """
        Log an internal message using Qgis's log function
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

        QgsMessageLog.logMessage(String, "EggAGGIS", level=lvl)

    def error(self, String, level, Bold=None, duration=None):
        """
        Display an Message Bar on the QGIS Screen, Used internally for Ease of logging.
        :param String: Message you wish to display
        :param level: Message Importance/Severity (0-2 | 0=Info | 1=Warning | 2=Critical)
        :param Bold: The Bold text displayed (If none it defaults to the Message Severity)
        :param duration: How long the Message is displayed to the user
        :return: None
        """

        if self.iface is None:
            self.log(
                "DEVELOPER ERROR, ATTEMPT TO CALL ERROR WITHOUT IFACE REFERENCE | Handling this error by passing data to log",
                2)
            self.log(String, level)
            return

        if Bold is not None:
            bld = Bold
        else:
            bld = None

        lvl = None
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

        if duration is not None:
            self.iface.messageBar().pushMessage(bld, String, level=lvl, duration=duration)

        else:
            self.iface.messageBar().pushMessage(bld, String, level=lvl)
