
import csv
from UseCommunication import Communicate

class IOParse:

    def __init__(self, path, iface):
        self.iface = iface
        self.com = Communicate(self.iface)
        try:
            self.csvFile = open(path, 'rb')
        except IOError:
            self.com.error(Bold="IOerror", String="Could not load given File", level=2)
        except:
            self.com.error(Bold="Unknown Error", String="An Unknown Error occured (See log for details", level=2)
            self.com.log("IOPARSE Encountered an Unknown error attempting to initialize self.csvFile", level=2)

    def ReadFile(self):
        reader = csv.reader(self.csvFile)

        for i in reader:
            self.com.log(i, level=0)
