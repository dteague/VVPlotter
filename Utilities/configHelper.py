import ROOT as r
import argparse
import os
import time

def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="Input root file (output of makeHistFile.py)")
    parser.add_argument("-a", "--analysis", type=str, required=True,
                        help="Specificy analysis used")
    parser.add_argument("-p", "--path", type=str, default='',
                        help="Extra path (defaults to day)")
    parser.add_argument("--drawStyle", type=str, default='stack', help='Way to draw graph',
                        choices=['stack', 'compare', 'sigratio'])
    parser.add_argument("-c", "--channels", type=str, default="all",
                        help="List (separate by commas) of channels to plot")
    parser.add_argument("-sig", "--signal", type=str, default='',
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
    
    return parser.parse_args()



def getNormedHistos(inFile, info, histName, chan):
    groupHists = dict()
    inFile.cd()
    
    for dir in inFile.GetListOfKeys():
        sample = dir.GetName()
        r.gDirectory.cd(sample)
        hist = r.gDirectory.Get("%s_%s" % (histName, chan))
        if not hist: continue
        groups = info.getGroupName(sample)
        if hist.Integral() <= 0:
            inFile.cd()
            continue
        
        if "Rebin" in info.getPlotSpec(histName):
            hist.Rebin(info.getPlotSpec(histName)["Rebin"])
        addOverflow(hist, info.getUpBinUser(histName))
        hist.Scale(info.getXSec(sample) / info.getSumweight(sample))
        for group in groups:
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

def addOverflow(inHist, highRange=None):
    lowbin = inHist.GetNbinsX()
    highbin = lowbin + 1
    
    if highRange:
        lowbin = inHist.FindBin(highRange)
        if highRange == inHist.GetXaxis().GetBinLowEdge(lowbin): lowbin -= 1
        extra = inHist.Integral(lowbin+1, highbin)
    else:
        extra = inHist.GetBinContent(highbin)
    
    inHist.SetBinContent(lowbin, inHist.GetBinContent(lowbin) + extra)
    for i in range(lowbin+1, highbin+1):
        inHist.SetBinContent(i, 0)
    
def getDrawOrder(groupHists, drawObj, info, ex=[]):
    """Might rename: sorts histograms based on integral and returns list
       of pairs with the first the group name and the second the root hist"""
    drawTmp = list()
    for key in drawObj:
        if key in ex: continue
        try:
            drawTmp.append((groupHists[key].Integral(), key))
        except:
            print("Missing the histograms for the group %s" % key)
            exit(0)
    
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
    
 
def checkOrCreateDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def printDrawObjAndExit(info):
    """Automatically give you drawObjs dictionary for you. Only works if drawObj=None"""
    print("you have no list of drawObjs, paste this into the code to continue\n")
    groups = info.getGroups()
    print("drawObj = {")
    for group in groups:
        print( '           %-12s: "%s",' % ('"'+group+'"', info.getStyle(group)))
    print("}")
    exit()


def setupPathAndDir(analysis, drawStyle, path, chans):
    """Setup HTML directory area and return path made"""
    extraPath = time.strftime("%Y_%m_%d")
    if path:
        extraPath = path+'/'+extraPath

    if 'hep.wisc.edu' in os.environ['HOSTNAME']:
        basePath = '%s/public_html' % (os.environ['HOME'])
    elif 'uwlogin' in os.environ['HOSTNAME'] or 'lxplus' in os.environ['HOSTNAME']:
        basePath = '/eos/home-{0:1.1s}/{0}/www'.format(os.environ['USER'])
    basePath += '/%s/%s/%s_%s' % ('PlottingResults', analysis, extraPath, drawStyle)

    for chan in chans:
        if chan == "all":
            chan = ""
        
        checkOrCreateDir('%s/%s' % (basePath,chan))
        checkOrCreateDir('%s/%s/plots' % (basePath,chan))
        checkOrCreateDir('%s/%s/logs' % (basePath,chan))
    return basePath
