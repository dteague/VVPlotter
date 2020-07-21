import numpy as np
from copy import deepcopy
from scipy.stats import beta

class GenericHist:
    def __init__(self, hist=[None, None], err2=[0.], under=0, over=0):
        self.hist = hist[0]
        self.bins = hist[1]
        if self.bins is not None and err2 == [0.]:
            err2 = np.zeros(len(self.bins) + 1)
        self.histErr2 = np.array(err2[1:-1])
        self.underflow = np.array([under, err2[0]])
        self.overflow = np.array([over, err2[-1]])

    @classmethod
    def fromUproot(cls, hist):
        if np.array(hist._fSumw2).size == 0:
            return cls()
        return cls(hist=hist.numpy(), err2=hist._fSumw2, under=hist.underflows,
                   over=hist.overflows)

    def copy_into(self, hist):
        for var in ["hist", "bins", "histErr2", "underflow", "overflow"]:
            setattr(self, var, getattr(hist, var))

    def copy(self):
        return deepcopy(self)

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
        self.underflow[1] *= scale
        self.overflow[1] *= scale

    def empty(self):
        return self.bins is None

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

    def changeAxis(self, newRange):
        lowIdx = 0
        highIdx = self.bins.size
        for i, val in enumerate(self.bins):
            if val <= newRange[0]:
                lowIdx = i
            if val >= newRange[1]:
                highIdx = i
                break
        self.changeAxisIndex(lowIdx, highIdx)

    def changeAxisIndex(self, lowIdx, highIdx):
        self.bins = self.bins[lowIdx:highIdx+1]
        self.overflow[0] += sum(self.hist[highIdx:])
        self.overflow[1] += sum(self.histErr2[highIdx:])
        self.underflow[0] += sum(self.hist[:lowIdx])
        self.underflow[1] += sum(self.histErr2[:lowIdx])
        self.hist = self.hist[lowIdx:highIdx]
        self.histErr2 = self.histErr2[lowIdx:highIdx]


    def rebin(self, rebin):
        if not isinstance(rebin, int):
            self.special_rebin(rebin)
            return (-1, -1)
        origRebin = rebin
        size = len(self.hist)
        subSize = size//rebin
        newSize = subSize * rebin
        if newSize == 0:
            print("New binning is too fine:")
            print("Rebin: {}, Old # bins: {}".format(rebin, size))
            raise Exception
        elif float(newSize)/size < 0.95:
            while float(newSize)/size < 0.975:
                rebin -= 1
                subSize = size//rebin
                newSize = subSize * rebin

        self.changeAxisIndex(0, newSize)
        self.hist = np.sum(self.hist.reshape(rebin, subSize), axis=1)
        self.histErr2 = np.sum(self.histErr2.reshape(rebin, subSize), axis=1)
        self.bins = self.bins[::subSize]

        return (origRebin, rebin)

    def special_rebin(self, rebin):
        old_width = self.bins[1] - self.bins[0]
        i = 0
        new_bins = [self.bins[0]]
        new_hist = list()
        new_histErr2 = list()
        for num, width in rebin:
            if width > 0:
                bin_width = int(width/old_width+0.5)
            else:
                bin_width = int((len(self.bins)-i-1)/num) + 1
            while i + bin_width < len(self.bins) and num > 0:
                num -= 1
                new_bins.append(self.bins[i+bin_width])
                new_hist.append(sum(self.hist[i:i+bin_width]))
                new_histErr2.append(sum(self.histErr2[i:i+bin_width]))
                i += bin_width
        new_bins.append(self.bins[-1])
        new_hist.append(sum(self.hist[i:]))
        new_histErr2.append(sum(self.histErr2[i:]))
        self.bins = np.array(new_bins)
        self.hist = np.array(new_hist)
        self.histErr2 = np.array(new_histErr2)
        
    def integral(self):
        return np.sum(self.hist)

    def get_int_err(self, sqrt_err=False):
        if sqrt_err:
            return np.array([np.sum(self.hist), np.sqrt(np.sum(self.histErr2))])
        else:
            return np.array([np.sum(self.hist), np.sum(self.histErr2)])

    def getMyTH1(self):
        full_hist = np.concatenate(([self.underflow[0]], self.hist, [self.overflow[0]]))
        full_hist_err2 = np.concatenate(([self.underflow[1]], self.histErr2, [self.overflow[1]]))
        return (self.bins, full_hist, full_hist_err2)


    def divide(self, denom):
        size = len(self.hist)

        p_raw = np.divide(self.hist**2, self.histErr2, out=np.zeros(size),
                          where=self.histErr2!=0)
        t_raw = np.divide(denom.hist**2, denom.histErr2, out=np.zeros(size),
                          where=denom.histErr2!=0)
        ratio = np.divide(self.histErr2*denom.hist, self.hist*denom.histErr2,
                         out=np.zeros(size), where=self.hist*denom.histErr2!=0)

        alf = (1-0.682689492137)/2
        lo = np.array([beta.ppf(alf, p, t+1) for p, t in zip(p_raw, t_raw)])
        hi = np.array([beta.ppf(1 - alf, p+1, t) for p, t in zip(p_raw, t_raw)])
        lo[np.isnan(lo)] = 0
        hi[np.isnan(hi)] = 0
        self.hist = np.divide(self.hist, denom.hist, out=np.zeros(size),
                              where=denom.hist!=0)

        errLo = self.hist - ratio*lo/(1-lo)
        errHi = ratio*hi/(1-hi) - self.hist
        self.histErr2 = (errLo**2 + errHi**2)/2
        return self
