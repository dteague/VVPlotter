import ROOT as r
import numpy as np

class pyHist:
    def __init__(self, name, rootHist, color):
        self.name = name
        self.leftEdge = list()
        self.yVal = list()
        self.nBins = rootHist.GetNbinsX()
        self.width = rootHist.GetBinWidth(1)
        self.underflow = rootHist.GetBinContent(0)
        self.overflow = rootHist.GetBinContent(self.nBins)
        for i in range(1, rootHist.GetNbinsX()+1):
            self.leftEdge.append(rootHist.GetBinLowEdge(i))
            self.yVal.append(rootHist.GetBinContent(i))
        self.color = color

    def getNbins(self):
        return self.nBins

    def getBins(self):
        return np.array(self.leftEdge)

    def getValues(self):
        return np.array(self.yVal)



