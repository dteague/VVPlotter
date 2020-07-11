from .pyUproot import GenericHist

from matplotlib import colors as clr
import numpy as np
from copy import deepcopy

class pyStack():
    def __init__(self, drawOrder, isMult=False):
        self.stack = list()
        self.colors = list()
        self.edgecolors = list()
        self.names = list()
        self.fancyNames = None
        self.bins = drawOrder[0][1].bins
        self.title = drawOrder[0][1].name
        self.hists = list()
        self.histTotal = GenericHist()
        if isMult:
            self.bins = self.bins - 0.5
        #self.align = 'left' if isMult else "mid"
        self.align = "mid"
        self.title = None
        self.options = {"stacked": True, "histtype": "stepfilled"}

        for name, hist in drawOrder:
            self.names.append(name)
            self.hists.append(deepcopy(hist))
            self.stack.append(hist.hist)
            self.histTotal += hist

    def setColors(self, colorMap):
        for name in self.names:
            self.colors.append(colorMap[name])
            self.edgecolors.append(self._darkenColor(colorMap[name]))

    def setLegendNames(self, info):
        self.fancyNames = list()
        for name in self.names:
            fName = info.getLegendName(name)
            if '\\' in fName:
                fName = r'$%s$' % fName
            self.fancyNames.append(fName)

    def _darkenColor(self, color):
        cvec = clr.to_rgb(color)
        dark = 0.3
        return tuple([i - dark if i > dark else 0.0 for i in cvec])

    def getHist(self):
        return self.histTotal

    def setDrawType(self, drawtype):
        if drawtype == "compare":
            self.options["stacked"] = False
            self.options["histtype"] = "step"
            self.edgecolors = self.colors

    def _getXVal(self):
        return [self.bins[:-1]] * len(self.stack)

    def getRange(self):
        if self.bins[0] < 0:
            return (self.bins[0], self.bins[-1])

        for highBin, val in zip(self.bins[::-1], self.histTotal.hist[::-1]):
            if val > 0.:
                return (self.bins[0], highBin)

    def getInputs(self, **kwargs):
        rDict = dict(
            {
                "weights": self.stack,
                "x": self._getXVal(),
                "bins": self.bins,
                "color": self.colors,
                "label": self.fancyNames,
                'align': self.align,
            }, **self.options)
        rDict.update(kwargs)
        return rDict

    def applyPatches(self, plot, patches):
        for p, ec in zip(patches, self.edgecolors):
            plot.setp(p, edgecolor=ec)
