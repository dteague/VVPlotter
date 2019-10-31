import ROOT as r
from MyObject import MyObject

class MyRatio(MyObject, object):
    def __init__(self, drawStyle, stack, signal=None, data=None):
        super(MyRatio, self).__init__()
        if drawStyle == 'compare' and signal:
            self.myObj = r.TRatioPlot(stack, signal)
            self.yUpTitle = "a.u."
            self.yDownTitle = "sig/MC"
        elif drawStyle == 'stack' and data:
            self.myObj = r.TRatioPlot(stack, data)
            self.yUpTitle = "Events/bin"
            self.yDownTitle = "Data/MC"
        elif drawStyle == 'sigratio' and signal:
            self.myObj = r.TRatioPlot(stack, signal)
            self.yUpTitle = "Events/bin"
            self.yDownTitle = "Signal/MC"
        # So you don't get a weird border
        if self.myObj:
             self.myObj.SetRightMargin(0.04)
             self.myObj.SetLeftMargin(0.11)
             self.myObj.SetUpTopMargin(0.07)
             self.myObj.SetSeparationMargin(0.01)
             
    def setAttributes(self):
       

        # self.myObj.GetLowerRefYaxis().SetRangeUser(0,2)
        self.myObj.GetLowerRefGraph().SetLineWidth(2)
        self.myObj.GetLowerRefYaxis().SetNdivisions(505)
        self.myObj.GetUpperRefObject().SetMinimum(0.0001)
        self.myObj.GetUpperRefYaxis().SetTitle(self.yUpTitle)
        self.myObj.GetLowerRefYaxis().SetTitle(self.yDownTitle)
        tmplower =self.myObj.GetLowerRefGraph().
        
    def getUpperPad(self):
        return self.myObj.GetUpperPad()

    def setMax(self, maxVal):
        self.myObj.GetUpperRefObject().SetMaximum(maxVal)

    
    def isValid(self):
        return bool(self.myObj)

