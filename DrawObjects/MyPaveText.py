import ROOT as r
from MyObject import MyObject

class MyPaveText(MyObject, object):
    def __init__(self, lumi):
        super(MyPaveText,self).__init__()
        self.lumiText = "%f fb^{-1}" % lumi if lumi>0 else ""
        self.lumiText += " (13 TeV)"
        

        self.myObj = r.TLatex()
        self.myObj.SetNDC();
        self.myObj.SetTextAngle(0);
        self.myObj.SetTextColor(r.kBlack);    


    def getAndDraw(self, pad, extraText = ""):
        pad.cd()
        top = pad.GetTopMargin()
        left = pad.GetLeftMargin()
        right = pad.GetRightMargin()
        bot = pad.GetBottomMargin()

        lumiX = 1 - right
        lumiY = (1 - top) + 0.2*top
        cmsX = left + 0.045*(1 - left - right);
        cmsY = (1 - top) - 0.075*(1 - top - bot)
        extraY = cmsY - 0.75*top
        
        # Lumi
        self.setAttributes(42, 31, 0.6*top)
        self.myObj.DrawLatex(lumiX, lumiY, self.lumiText)

        # CMS
        self.setAttributes(61, 11, 0.75*top)
        self.myObj.DrawLatex(cmsX, cmsY, "CMS")
        
        # Extra
        if extraText:
            self.setAttributes(52, 11, 0.75*0.76*top)
            self.myObj.DrawLatex(cmsX, extraY, extraText)

        return self.myObj

    def setAttributes(self, font, align, size):
        self.myObj.SetTextFont(font)
        self.myObj.SetTextAlign(align)
        self.myObj.SetTextSize(size)
                    

        
