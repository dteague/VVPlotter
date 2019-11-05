import ROOT as r
import numpy as np
from matplotlib import colors

class pyHist:
    def __init__(self, name, rootHist, color, isTH1=True, isMult=False):
        self.name = name
        self.x = list()
        self.y = list()
        self.yerr = list()
        self.xerr = list()
        self.hist = rootHist.Clone()
        self.color = color
        
        if '\\' in self.name:
                self.name = r'$%s$' % self.name
            
        if isTH1:
            self.setupTH1(rootHist, isMult)
        else:
            self.setupTGraph(rootHist, isMult)
        
    def setupTH1(self, rootHist, isMult):
        width = rootHist.GetBinWidth(1) if isMult else 0.0
        
        for i in range(1, rootHist.GetNbinsX()+1):
            if rootHist.GetBinContent(i) <= 0:
                continue
            self.x.append(rootHist.GetBinCenter(i)-width/2)
            self.y.append(rootHist.GetBinContent(i))
            self.yerr.append(rootHist.GetBinError(i))
        self.xerr = [rootHist.GetBinWidth(1)/2]*len(self.x)

    def setupTGraph(self, rootGraph, isMult):
        width = rootGraph.GetErrorX(0) if isMult else 0.0
        x, y = r.Double(0), r.Double(0)
        for i in range(rootGraph.GetN()):
            rootGraph.GetPoint(i, x, y)
            self.x.append(float(x)-width)
            self.y.append(float(y))
            self.yerr.append(rootGraph.GetErrorY(i))
            self.xerr.append(rootGraph.GetErrorX(i))
        
    def getRHist(self):
        return self.hist

        
    def getInputs(self, **kwargs):
        return dict({"x":self.x, "xerr":self.xerr, "y":self.y, "yerr":self.yerr, "ecolor":self.color, "color":self.color, "barsabove":True, "label":self.name,},  **kwargs)

