import numpy as np
from copy import deepcopy

from Utilities.pyUproot import GenericHist

class pyHist(GenericHist):
    def __init__(self, name, color, isMult):
        super().__init__()
        self.name = name
        self.color = color
        self.align = 'mid'
        if '\\' in self.name:
            self.name = r'${}$'.format(self.name)
        self.isMult = isMult
            
    def copy_into(self, hist):
        prev_bins = self.bins
        super().copy_into(hist)
        if prev_bins is None:
            self.xerr = (self.bins[1:] - self.bins[:-1])/2
            self.x = self.bins[:-1] if self.isMult else self.xerr + self.bins[:-1]
            if self.isMult:
                self.bins = self.bins - 0.5
            
    def scaleHist(self, scale):
        self.scale(scale)
        if scale != 1:
            self.name += " x " + str(scale)
        

    def getInputs(self, **kwargs):
        return dict({"x": self.x, "xerr": self.xerr, "y": self.hist,
                     "yerr": np.sqrt(self.histErr2), "ecolor": self.color,
                     "color": self.color, "barsabove": True, "label": self.name,},
                    **kwargs)

    def getInputsHist(self, **kwargs):
        return dict({"weights": self.hist, "x": self.x, "bins": self.bins,
                     "color": self.color, 'align': self.align, "histtype": "step"},
                    **kwargs)
