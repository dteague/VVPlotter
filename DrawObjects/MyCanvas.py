import ROOT as r
from MyObject import MyObject

class MyCanvas(MyObject, object):
    def __init__(self, histName):
        super(MyCanvas,self).__init__()
        dimensions = (800, 800)
        self.myObj = r.TCanvas(histName, histName)

    def setAttributes(self):
        pass

    def writeOut(self, outFile):
        outFile.cd()
        self.myObj.Write()


        
