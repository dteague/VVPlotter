import ROOT as r
import numpy as np
from matplotlib import colors

class pyHist:
    def __init__(self, name, rootHist, color, isTH1=True):
        self.name = name
        self.x = list()
        self.y = list()
        self.yerr = list()
        self.xerr = list()
        self.underflow = 0.
        self.overflow = 0.
        self.hist = rootHist.Clone()
        self.color = color

        if '\\' in self.name:
                self.name = r'$%s$' % self.name
            
        
        if isTH1:
            self.setupTH1(rootHist)
        else:
            self.setupTGraph(rootHist)
        
    def setupTH1(self, rootHist):
        width = rootHist.GetBinWidth(1)
        self.underflow = rootHist.GetBinContent(0)
        self.overflow = rootHist.GetBinContent(rootHist.GetNbinsX())
        for i in range(1, rootHist.GetNbinsX()+1):
            if rootHist.GetBinContent(i) <= 0:
                continue
            self.x.append(rootHist.GetBinCenter(i)-width/2)
            self.y.append(rootHist.GetBinContent(i))
            self.yerr.append(rootHist.GetBinError(i))
            self.xerr.append(width/2)

    def setupTGraph(self, rootGraph):
        width = rootGraph.GetErrorX(0)
        x, y = r.Double(0), r.Double(0)
        for i in range(rootGraph.GetN()):
            rootGraph.GetPoint(i, x, y)
            self.x.append(float(x)-width)
            self.y.append(float(y))
            self.yerr.append(rootGraph.GetErrorY(i))
            self.xerr.append(rootGraph.GetErrorX(i))
        print self.x
            
    def getRHist(self):
        return self.hist

        
    def getInputs(self):
        return {"x":self.x, "xerr":self.xerr, "y":self.y, "yerr":self.yerr, "ecolor":self.color, "color":self.color, "barsabove":True, "label":self.name, "fmt":'o', "markersize":4}

