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
        self.draw_sc = 1.
        
    def copy_into(self, hist):
        super().copy_into(hist)
        self.xerr = (self.bins[1:] - self.bins[:-1])/2
        self.x = self.bins[:-1] if self.isMult else self.xerr + self.bins[:-1]
        
    def scaleHist(self, scale):
        self.draw_sc = scale
        if scale != 1:
            self.name += " x " + str(scale)

    def getInputs(self, **kwargs):
        return dict({"x": self.x, "xerr": self.xerr, "y": self.draw_sc*self.hist,
                     "yerr": self.draw_sc*np.sqrt(self.histErr2),
                     "ecolor": self.color, "color": self.color, "barsabove": True,
                     "label": self.name,}, **kwargs)

    def getInputsHist(self, **kwargs):
        bins = self.bins - 0.5 if self.isMult else self.bins
        return dict({"weights": self.draw_sc*self.hist, "x": self.x, "bins": bins,
                     "color": self.color, 'align': self.align,"histtype": "step"},
                    **kwargs)
