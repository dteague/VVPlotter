import ROOT as r
from MyObject import MyObject
import subprocess

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

    def saveAsPDF(self,path):
        outputName = "%s/%s" % (path, self.myObj.GetName())
        self.myObj.Print(outputName + ".png")
        subprocess.call(["convert", "%s.png"%outputName, "%s.pdf"%outputName])
        
        
