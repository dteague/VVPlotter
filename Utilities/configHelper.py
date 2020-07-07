import argparse
import os
import time
from Utilities.pyUproot import GenericHist


def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="Input root file (output of makeHistFile.py)")
    parser.add_argument("-a", "--analysis", type=str, required=True,
                        help="Specificy analysis used")
    parser.add_argument("-p", "--path", type=str, default='',
                        help="Extra path (defaults to day)")
    parser.add_argument("--drawStyle", type=str, default='stack',
                        help='Way to draw graph',
                        choices=['stack', 'compare', 'sigratio'])
    parser.add_argument("-c", "--channels", type=str,
                        default="all", help="List (separate by commas) of channels to plot")
    parser.add_argument("-sig", "--signal", type=str, default='',
                        help="Name of the group to be made into the Signal")
    parser.add_argument("-j", type=int, default=1, help="Number of cores")
    parser.add_argument("-l", "--lumi", type=float, default=35.9,
                        help="Luminsoity in fb-1. Default 35.9 fb-1. "
                        "Set to -1 for unit normalization")
    parser.add_argument("--logy", action='store_true',
                        help="Use logaritmic scale on Y-axis")
    parser.add_argument("--stack_signal", action='store_true',
                        help="Stack signal hists on top of background")
    parser.add_argument("--ratio_range", nargs=2, default=[0.4, 1.6],
                        help="Ratio min ratio max (default 0.5 1.5)")
    parser.add_argument("--no_ratio", action="store_true",
                        help="Do not add ratio comparison")
    parser.add_argument("--autoScale", type=float, default=-1.,
                        help="Ignore Max argument and scale max to ratio given")
    parser.add_argument("--info", type=str, default="plotInfo.py",
                        help="Name of file containing histogram Info")
    return parser.parse_args()


def getNormedHistos(inFile, info, histName, chan):
    groupHists = dict()
    oldRebin = None
    fullHistName = "{}_{}".format(histName, chan)
    for sample in inFile.keys():
        sample = sample[:-2] if sample[-2:] == ";1" else sample

        if fullHistName not in inFile[sample]: continue
        rootHist = inFile[sample][fullHistName]
        scale = info.getXSec(sample) / info.getSumweight(sample)

        hist = GenericHist(rootHist, scale)
        if hist.empty():
            continue

        if "setXaxis" in info.getPlotSpec(histName):
            hist.changeAxis(info.getPlotSpec(histName)["setXaxis"])
        if "Rebin" in info.getPlotSpec(histName):
            oldRebin, newRebin = hist.rebin(info.getPlotSpec(histName)["Rebin"])
        
        hist.addOverflow()
        
        for group in info.getGroupName(sample):
            if group not in groupHists.keys():
                groupHists[group] = GenericHist()
            groupHists[group] += hist
            groupHists[group].name = group

    if oldRebin and oldRebin - newRebin > 5:
        print("Large change in rebin for {}: {} to {}".format(histName, oldRebin, newRebin))
            
    for name, hist in groupHists.iteritems():
        if info.getLumi() < 0:
            scale = 1 / sum(hist.hist)
            hist.scale(scale)
        else:
            hist.scale(info.getLumi())

    return groupHists


def getDrawOrder(groupHists, drawObj, info, ex=[]):
    """Might rename: sorts histograms based on integral and returns list
       of pairs with the first the group name and the second the root hist"""
    drawTmp = list()
    for key in drawObj:
        if key in ex: continue
        try:
            drawTmp.append((sum(groupHists[key].hist), key))
        except:
            print("Missing the histograms for the group %s" % key)
            exit(0)

    drawTmp.sort()
    return [(i[1], groupHists[i[1]]) for i in drawTmp]


from math import log10


def findScale(s, b):
    scale = 1
    prevS = 1
    while b // (scale * s) != 0:
        prevS = scale
        if int(log10(scale)) == log10(scale):
            scale *= 5
        else:
            scale *= 2
    return prevS


def findScale(ratio):
    sigNum = 10**int(log10(ratio))
    return int((ratio) / sigNum) * sigNum


def checkOrCreateDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def printDrawObjAndExit(info):
    """Automatically give you drawObjs dictionary for you. Only works if drawObj=None"""
    print(
        "you have no list of drawObjs, paste this into the code to continue\n")
    groups = info.getGroups()
    print("drawObj = {")
    for group in groups:
        print('          "%-12s": "%s",' % (group, info.getStyle(group)))
    print("}")
    exit()


def setupPathAndDir(analysis, drawStyle, path, chans):
    """Setup HTML directory area and return path made"""
    extraPath = time.strftime("%Y_%m_%d")
    if path:
        extraPath = path + '/' + extraPath

    if 'hep.wisc.edu' in os.environ['HOSTNAME']:
        basePath = '{}/public_html'.format(os.environ['HOME'])
    elif 'uwlogin' in os.environ['HOSTNAME'] or 'lxplus' in os.environ['HOSTNAME']:
        basePath = '/eos/home-{0:1.1s}/{0}/www'.format(os.environ['USER'])
    basePath += '/PlottingResults/{}/{}_{}'.format(analysis, extraPath,
                                                   drawStyle)
    # for all directory
    checkOrCreateDir('{}/plots'.format(basePath))
    checkOrCreateDir('{}/logs'.format(basePath))
    for chan in chans:
        if "all": continue
        path = "{}/{}".format(basePath, chan)
        checkOrCreateDir(path)
        checkOrCreateDir('{}/plots'.format(path))
        checkOrCreateDir('{}/logs'.format(path))
    return basePath


import shutil


def copyDirectory(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
