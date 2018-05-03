
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
        self.ValueTypes = None
        self.Final = []

    def ReadFile(self):
        reader = csv.reader(self.csvFile)
        self.com.log(str(reader), level=0)
        """
        Assume First row is the Values, Each row after that is each data point
        
        Using a Key pair store Within a list
        would look like
        
        [{"lat" : value, "Long" : value ... }, {"lat" : Value, "Long" : value ...},...]
        
        Current input looks like:
        ["lat", "long,....],
        [132, 1322, ...],
        [...],...
        """
        """
        
        for idx, val in enumerate(reader):
            for idxi, vali in enumerate(val):
                if idx == 0:
                    FinalOutput.append(vali)
                else:
                    FinalOutput[idx-1]"""
        self.ValueTypes = reader[0]

        for idx, val in enumerate(reader):
            if idx == 0:
                continue
            else:
                self.Final.append(val)

    def PlotPoints(self):
        



