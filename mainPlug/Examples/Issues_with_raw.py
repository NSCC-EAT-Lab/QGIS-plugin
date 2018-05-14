import os
import sys
import win32api


"""
This is the issue with working with file pathing currently

Note the raw input that is the issue
"""


x = (os.path.expanduser('~') + "/tmp/" + "ack" + "temp2.sdat")

p = {"path":"%r"%x}

y = [p["path"]]

print x +"\n"

print p["path"]

print y[0]