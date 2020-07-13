from matplotlib import colors as clr
from .pyUproot import GenericHist
import numpy as np


class pyErrors(GenericHist):
    def __init__(self, name, color, isMult):
        super().__init__()
        self.name = name
        self.color = color
        self.isMult = isMult
    
    def copy_into(self, hist):
        super().copy_into(hist)
        
    def getInputs(self, **kwargs):
        bins = self.bins - 0.5 if self.isMult else self.bins
        bottom = self.hist - np.sqrt(self.histErr2)
        return dict({"weights": 2*np.sqrt(self.histErr2), "x": self.bins[:-1],
                     "bins": bins, 'bottom': bottom, "histtype": 'stepfilled',
                     "color": self.color,'align': 'mid', 'stacked': True,
                     "hatch": '//', "alpha": 0.4, "label":self.name},
                    **kwargs)
