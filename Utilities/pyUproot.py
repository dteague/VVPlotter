import numpy as np
from copy import deepcopy


class GenericHist:
    def __init__(self, *args):

        self.bins = None
        self.name = None

        if len(args) == 0:
            return

        hist = args[0]
        from ROOT import TGraphAsymmErrors
        if isinstance(hist, TGraphAsymmErrors):
            self.setupTGraph(hist)
        else:
            scale = 1 if len(args) == 1 else args[1]
            if np.array(hist.fSumw2).size == 0:
                return
            self.hist = scale * np.array(hist.numpy[0])
            self.bins = np.array(hist.numpy[1])
            self.histErr2 = scale**2 * np.array(hist.fSumw2[1:-1])
            self.underflow = np.array(
                [scale * hist.underflows, scale**2 * hist.fSumw2[0]])
            self.overflow = np.array(
                [scale * hist.overflows, scale**2 * hist.fSumw2[-1]])

    def __add__(self, other):
        if self.empty():
            return deepcopy(other)
        if not (self.bins == other.bins).all():
            raise Exception("GenericHist: Different bin size")
        returnHist = GenericHist()
        returnHist.bins = np.array(self.bins)
        returnHist.hist = np.array(self.hist + other.hist)
        returnHist.histErr2 = np.array(self.histErr2 + other.histErr2)
        returnHist.underflow = self.underflow + other.underflow
        returnHist.overflow = self.overflow + other.overflow
        returnHist.name = self.name
        return returnHist

    def scale(self, scale):
        self.hist *= scale
        self.histErr2 *= scale**2
        self.underflow *= scale
        self.overflow *= scale

    def empty(self):
        return self.bins is None

    def getTH1(self):
        from ROOT import TH1D
        rHist = TH1D(self.name, self.name, len(self.bins) - 1, self.bins)
        i = 1
        for val, err in zip(self.hist, np.sqrt(self.histErr2)):
            rHist.SetBinContent(i, val)
            rHist.SetBinError(i, err)
            i += 1
        return rHist

    def setupTGraph(self, graph):
        self.hist = np.array(graph.GetY())
        self.histErr2 = list()
        self.bins = [graph.GetX()[0] - graph.GetErrorX(0)]
        self.underflow = np.array([0, 0])
        self.overflow = np.array([0, 0])

        for i in range(graph.GetN()):
            self.histErr2.append(graph.GetErrorY(i)**2)
            self.bins.append(2 * graph.GetErrorX(i) + self.bins[-1])

        self.histErr2 = np.array(self.histErr2)
        self.bins = np.array(self.bins)

    def addOverflow(self):
        self.hist[-1] += self.overflow[0]
        self.histErr2[-1] += self.overflow[1]
        self.overflow = np.array([0., 0.])

    def addUnderflow(self):
        self.hist[0] += self.underflow[0]
        self.histErr2[0] += self.underflow[1]
        self.underflow = np.array([0., 0.])

    def rebin(self, rebin):
        size = len(self.hist)
        if size // rebin != size / rebin:
            print("bad rebinning! Rebin {} but size is {}".format(rebin, size))
            raise Exception
        self.hist = np.sum(self.hist.reshape(rebin, size / rebin), axis=1)
        self.histErr2 = np.sum(self.histErr2.reshape(rebin, size / rebin),
                               axis=1)
        self.bins = self.bins[::size / rebin]
