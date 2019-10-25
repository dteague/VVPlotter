import ROOT as r
from MyObject import MyObject

class MyRatio(MyObject, object):
    def __init__(self, drawStyle, stack, signal=None, data=None):
        super(MyRatio, self).__init__()
        if drawStyle == 'compare' and signal:
            self.myObj = r.TRatioPlot(stack, signal)
        elif drawStyle == 'ratio' and data:
            self.myObj = r.TRatioPlot(stack, data)

    def setAttributes(self):
        self.myObj.SetRightMargin(0.04)
        self.myObj.SetUpTopMargin(0.07)
        self.myObj.SetSeparationMargin(0.01)
        self.myObj.GetLowerRefYaxis().SetRangeUser(0,2)
        self.myObj.GetLowerRefGraph().SetLineWidth(2)
        self.myObj.GetLowerRefYaxis().SetNdivisions(505)
        self.myObj.GetUpperRefObject().SetMinimum(0.001)
        
        
    def getUpperPad(self):
        return self.myObj.GetUpperPad()

    def setMax(self, maxVal):
        self.myObj.GetUpperRefObject().SetMaximum(maxVal*1.3)

    
    def isValid(self):
        return bool(self.myObj)

