import ROOT as r
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib import colors as clr

class pyErrors:
    def __init__(self, name, rootHist, color, isTH1=True, isMult=False):
        self.name = name
        self.x = list()
        self.y = list()
        self.yerr = list()
        self.xerr = list()
        self.hist = rootHist.Clone()
        self.color = color
        self.edgecolor = self._darkenColor(self.color)
        # self.align = 'left' if isMult else "mid"
        self.align = 'mid'
        if isTH1:
            self.setupTH1(rootHist, isMult)
        else:
            self.setupTGraph(rootHist, isMult)

        self.bottom = [y - yerr for y, yerr in zip(self.y, self.yerr)]
        self.errors = [2*yerr for yerr in self.yerr]
        self.bins   = [x - xerr for x, xerr in zip(self.x, self.xerr)]
        self.bins.append(self.x[-1] + self.xerr[-1])
        
        print self.errors
        print self.bins
        print self.bottom
        
    def setupTH1(self, rootHist, isMult):
        width = rootHist.GetBinWidth(1) if isMult else 0.0
        
        self.underflow = rootHist.GetBinContent(0)
        self.overflow = rootHist.GetBinContent(rootHist.GetNbinsX()+1)
        for i in range(1, rootHist.GetNbinsX()+1):
            if rootHist.GetBinContent(i) <= 0:
                continue
            self.x.append(rootHist.GetBinCenter(i)-width/2)
            self.y.append(rootHist.GetBinContent(i))
            self.yerr.append(rootHist.GetBinError(i))
        self.y[0] += self.underflow
        self.y[-1] += self.overflow
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

    def _darkenColor(self, color):
        cvec = clr.to_rgba(color)
        dark = 0.3
        return tuple([i - dark if i > dark else 0.0 for i in cvec])

    def getInputs(self, **kwargs):
        return dict({"weights":self.errors, "x":self.x, "bins":self.bins, 'bottom':self.bottom, "histtype":'stepfilled', "color":self.color, 'align':self.align, }, **kwargs)

