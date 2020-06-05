import numpy as np
from matplotlib import colors
from Utilities.pyUproot import GenericHist
import math


class pyHist:
    def __init__(self, name, hist, color, isTH1=True, isMult=False):
        self.name = name
        self.hist = hist
        self.color = color
        #self.align = 'left' if isMult else "mid"
        self.align = 'mid'
        
        
        if '\\' in self.name:
            self.name = r'$%s$' % self.name

        if not isinstance(hist, GenericHist):
            hist = GenericHist(hist)

        self.setupTH1(hist, isMult)
        if isMult:
            self.xbins = self.xbins - 0.5
        
    def setupTH1(self, rootHist, isMult):
        self.xbins = rootHist.bins
        self.y = rootHist.hist
        self.yerr = np.sqrt(rootHist.histErr2)
        width = np.array([
            self.xbins[i + 1] - self.xbins[i]
            for i in xrange(len(self.xbins) - 1)
        ])
        self.xerr = width / 2
        self.x = self.xbins[:-1] if isMult else self.xerr + self.xbins[:-1]

    def getRHist(self):
        return self.hist.getTH1()

    def scaleHist(self, scale):
        self.y = np.multiply(self.y, scale)
        self.yerr = np.multiply(self.yerr, scale)
        if scale != 1:
            self.name += " x " + str(scale)
        self.hist.scale(scale)

    def getInputs(self, **kwargs):
        return dict(
            {
                "x": self.x,
                "xerr": self.xerr,
                "y": self.y,
                "yerr": self.yerr,
                "ecolor": self.color,
                "color": self.color,
                "barsabove": True,
                "label": self.name,
            }, **kwargs)

    def getInputsHist(self, **kwargs):
        return dict(
            {
                "weights": self.y,
                "x": self.x,
                "bins": self.xbins,
                "color": self.color,
                'align': self.align,
                "histtype": "step"
            }, **kwargs)
