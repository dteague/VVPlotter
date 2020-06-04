#!/usr/bin/env python
import Utilities.configHelper as config
args = config.getComLineArgs()

# need args before or root takes over "--help"
import os
import ROOT as r

from Utilities.InfoGetter import InfoGetter
from Utilities.pyHist import pyHist
from Utilities.pyStack import pyStack
from Utilities.pyErrors import pyErrors
from Utilities.pyPad import pyPad
from Utilities.LogFile import LogFile
from Utilities.makeSimpleHtml import writeHTML

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import sys
import time
import uproot

# run time variables
callTime = str(datetime.datetime.now())
command = ' '.join(sys.argv)
r.gErrorIgnoreLevel = r.kError

font = {
    'family': 'sans',
    'weight': 'normal',
}

plt.rc('font', **font)

SMALL_SIZE = 12
MEDIUM_SIZE = 16
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)
plt.rc('axes', labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=MEDIUM_SIZE)
plt.rc('ytick', labelsize=MEDIUM_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)

# Setup

drawObj = {
    #"tttt_"     : "mediumslateblue",
    "ttt": "crimson",
    "ttz": "mediumseagreen",
    "rare_no3top": "darkorange",
    "ttXY": "cornflowerblue",
    "ttw": "darkgreen",
    "xg": "indigo",
    "tth": "slategray",
    "other": "blue",
    "tttt_201X": "darkmagenta",
    # "ttt_201X"      : "cornflowerblue",
}

# In out
inFile = uproot.open(args.infile)

anaSel = args.analysis.split('/')
if len(anaSel) == 1:
    anaSel.append('')

info = InfoGetter(anaSel[0], anaSel[1], inFile, args.info)
if args.drawStyle == "compare":
    info.setLumi(-1)
else:
    info.setLumi(args.lumi * 1000)

info.setDrawStyle(args.drawStyle)
if not drawObj:
    config.printDrawObjAndExit(info)

if args.signal and args.signal not in drawObj:
    print("signal not in list of groups!")
    print(drawObj.keys())
    exit(1)
signalName = args.signal
channels = args.channels.split(',')

channels = ['SS']  #["all", "OS", "SS"]# , "mult", "one"]

basePath = config.setupPathAndDir(args.analysis, args.drawStyle, args.path,
                                  channels)

argList = list()
for histName in info.getListOfHists():
    if not info.isInPlotSpec(histName):
        continue
    argList.append((histName, info, basePath, args.infile, channels))

def makePlot(histName, info, basePath, infileName, channels):
    print("Processing {}".format(histName))
    isDcrt = info.isDiscreteGraph(histName)
    inFile = uproot.open(infileName)
    for chan in channels:
        signal, data, ratio, band, error = None, None, None, None, None

        #### FIX
        groupHists = config.getNormedHistos(inFile, info, histName, chan)
        # if not groupHists or groupHists.values()[0].InheritsFrom("TH2"):
        #     return

        exclude = []
        # signal
        if signalName in groupHists:
            signal = pyHist(info.getLegendName(signalName),
                            groupHists[signalName],
                            drawObj[signalName],
                            isMult=isDcrt)
            exclude.append(signalName)

        # data
        if False:
            data = pyHist("Data", groupHists['data'], 'black', isMult=isDcrt)
            exclude.append('data')

        drawOrder = config.getDrawOrder(groupHists,
                                        drawObj,
                                        info,
                                        ex=[signalName])
        stacker = pyStack(drawOrder, isMult=isDcrt)
        stacker.setColors(drawObj)
        stacker.setLegendNames(info)
        error = pyErrors("Stat Errors",
                         stacker.getHist(),
                         "plum",
                         isMult=isDcrt)
        if signal:
            scale = config.findScale(np.sum(stacker.stack) / sum(signal.y))
            #scale = config.findScale(max(signal.y), stacker.getRHist().GetMaximum())
            signal.scaleHist(scale)
        # ratio
        if signal:
            divide = r.TGraphAsymmErrors(signal.getRHist(), stacker.getRHist(),
                                         "pois")
            stack_divide = r.TGraphAsymmErrors(stacker.getRHist(),
                                               stacker.getRHist(), "pois")
            ratio = pyHist("Ratio",
                           divide,
                           "black",
                           isTH1=False,
                           isMult=isDcrt)
            band = pyErrors("Ratio",
                            stack_divide,
                            "plum",
                            isTH1=False,
                            isMult=isDcrt)

        # Extra options
        stacker.setDrawType(args.drawStyle)

        pad = pyPad(plt, ratio != None)

        n, bins, patches = pad.getMainPad().hist(**stacker.getInputs())
        stacker.applyPatches(plt, patches)

        if signal:
            pad.getMainPad().hist(**signal.getInputsHist())
            pad.getMainPad().errorbar(
                **signal.getInputs(fmt='o', markersize=4))
        if data:
            pad.getMainPad().errorbar(**data.getInputs(fmt='o', markersize=4))
        if error:
            pad.getMainPad().hist(
                **error.getInputs(hatch='//', alpha=0.4, label="Stat Error"))
        if ratio:
            pad.getSubMainPad().errorbar(
                **ratio.getInputs(fmt='o', markersize=4))
            pad.getSubMainPad().hist(**band.getInputs(
                hatch='//',
                alpha=0.4,
            ))

        pad.setLegend(info.getPlotSpec(histName))
        pad.axisSetup(info.getPlotSpec(histName), stacker.getRange())

        fig = plt.gcf()
        fig.set_size_inches(8, 8)

        if chan == "all" or len(channels) == 1:
            chan = ""
        baseChan = "{}/{}".format(basePath, chan)
        plotBase = "{}/plots/{}".format(baseChan, histName)
        plt.savefig("{}.png".format(plotBase),
                    format="png",
                    bbox_inches='tight')
        plt.savefig("{}.pdf".format(plotBase),
                    format="pdf",
                    bbox_inches='tight')
        plt.close()

        # setup log file
        logger = LogFile(histName, info, "{}/logs".format(baseChan))
        logger.addMetaInfo(callTime, command)
        logger.addMC(drawOrder)
        if signal:
            logger.addSignal(groupHists[signalName], signalName)
        logger.writeOut()


def makePlotStar(args):
    makePlot(*args)

import multiprocessing as mp
if args.j > 1:
    pool = mp.Pool(args.j)
    results = pool.map(makePlotStar, argList)
    pool.close()
    pool.join()
else:
    for plot in argList:
        makePlotStar(plot)

try:
    channels.remove("all")
except ValueError:
    if len(channels) == 1:
        channels = []
    else:
        print("No all channel")

writeHTML(basePath, args.analysis, channels)
for chan in channels:
    writeHTML("{}/{}".format(basePath, chan),
              "{}/{}".format(args.analysis, chan))
userName = os.environ['USER']
htmlPath = basePath[basePath.index(userName) + len(userName) + 1:]
if 'hep.wisc.edu' in os.environ['HOSTNAME']:
    print("https://www.hep.wisc.edu/~{0}/{1}".format(os.environ['USER'],
                                                         htmlPath[4:]))
else:
    print("https://{0}.web.cern.ch/{0}/{1}".format(os.environ['USER'],
                                                   htmlPath[4:]))


