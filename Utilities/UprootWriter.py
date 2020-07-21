import uproot_methods.classes.TH1

class SimpleNamespace (object):
    def __init__ (self, **kwargs):
        self.__dict__.update(kwargs)
    def __repr__ (self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))
    def __eq__ (self, other):
        return self.__dict__ == other.__dict__

class MyTH1(uproot_methods.classes.TH1.Methods, list):
    def __init__(self, bins, values, err2, title=""):
        self._fXaxis = SimpleNamespace()
        self._fXaxis._fNbins = len(values) - 2 
        self._fXaxis._fXmin = bins[0]
        self._fXaxis._fXmax = bins[-1]
        self._fXaxis._fXbins = bins
        self._fSumw2 = err2
        for x in values:
            self.append(float(x))
        self._fTitle = title
        self._classname = "TH1F"

import numpy as np
def get_hist(hist):
    return MyTH1(*hist.getMyTH1())
