import ROOT as r
import argparse

def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outfile", type=str, default="output.root",
                        help="Output root file name")
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="Input root file (output of makeHistFile.py)")
    parser.add_argument("-a", "--analysis", type=str, required=True,
                        help="Specificy analysis used")
    parser.add_argument("-s", "--selection", type=str, default="",
                        help="Specificy selection level to run over")
    parser.add_argument("--drawStyle", type=str, default='stack', help='Way to draw graph',
                        choices=['stack', 'compare'])
    parser.add_argument("-c", "--channels", type=str, default="all",
                        help="List (separate by commas) of channels to plot")
    parser.add_argument("-sig", "--signal", type=str, default="",
                        help="Name of the group to be made into the Signal")
    
    parser.add_argument("-l", "--lumi", type=float, default=35.9,
                        help="Luminsoity in fb-1. Default 35.9 fb-1. "
                        "Set to -1 for unit normalization")
    parser.add_argument("--logy", action='store_true',
                        help="Use logaritmic scale on Y-axis")
    parser.add_argument("--stack_signal", action='store_true',
                        help="Stack signal hists on top of background")
    parser.add_argument("--ratio_range", nargs=2, default=[0.4,1.6],
                        help="Ratio min ratio max (default 0.5 1.5)")
    parser.add_argument("--no_ratio", action="store_true",
                        help="Do not add ratio comparison")
    parser.add_argument("--autoScale", type=float, default=-1.,
                        help="Ignore Max argument and scale max to ratio given")
    
    
    # do nothing
    
    # parser.add_argument("--no_overflow", action='store_true',
    #                     help="No overflow bin")
    # parser.add_argument("-u", "--uncertainties", type=str, default="all",
    #                     choices=["all", "stat", "scale", "none"],
    #                     help="Include error bands for specfied uncertainties")
    # parser.add_argument("--nostack", action='store_true',
    #                     help="Don't stack hists")
    
    # parser.add_argument("--no_html", action='store_true',
    #                     help="Don't copy plot pdfs to website")
    # parser.add_argument("--no_data", action='store_true',
    #                     help="Plot only Monte Carlo")
    return parser.parse_args()



def getNormedHistos(inFile, info, histName, chan):
    groupHists = dict()
    inFile.cd()
    
    for dir in inFile.GetListOfKeys():
        sample = dir.GetName()
        r.gDirectory.cd(sample)
        hist = r.gDirectory.Get("%s_%s" % (histName, chan))
        group = info.getGroupName(sample)
        if hist.Integral() <= 0:
            inFile.cd()
            continue
        hist.Scale(info.getXSec(sample) / info.getSumweight(sample))
        if group not in groupHists.keys():
            groupHists[group] = hist.Clone()
        else:
            groupHists[group].Add(hist)
        inFile.cd()
    for name, hist in groupHists.iteritems():
        if info.getLumi() < 0:
            hist.Scale(1/hist.Integral())
        else:
            hist.Scale(info.getLumi())
        hist.SetName(name)
    return groupHists

def addOverflow(inHist):
    binMax = inHist.GetNbinsX()
    inHist.SetBinContent(binMax, inHist.GetBinContent(binMax) + inHist.GetBinContent(binMax+1) )
    
def getDrawOrder(groupHists, drawObj, info):
    drawTmp = [(hist.Integral(), key) for key, hist in groupHists.iteritems() if key in drawObj]
    drawTmp.sort()
    return [(i[1], groupHists[i[1]]) for i in drawTmp]


def getHistTotal(groupHists):
    totalHist = None
    for name, hist in groupHists:
        if not totalHist:
            totalHist = hist.Clone()
        else:
            totalHist.Add(hist)
    totalHist.SetName("error")
    return totalHist
    
def getMax(stack, signal=None, data=None):
    maxHeight = stack.GetMaximum()
    if signal:
        maxHeight = max(maxHeight, signal.GetMaximum())
    if data:
        maxHeight = max(maxHeight, data.GetMaximum())
    return maxHeight
    
 

