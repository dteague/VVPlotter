#!/usr/bin/env python
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mplhep as hep
import datetime
import sys
import time
import uproot
import multiprocessing as mp

from Utilities.InfoGetter import InfoGetter
from histograms import *
from Utilities.LogFile import LogFile
from Utilities.makeSimpleHtml import writeHTML
import Utilities.configHelper as config

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
plt.style.use(hep.style.CMS)

color_by_group = {
    #"tttt_"     : "mediumslateblue",
    "ttt": "crimson",
    "ttz": "mediumseagreen",
    "ttw": "darkgreen",
    "rare_no3top": "darkorange",
    "ttXY": "cornflowerblue",
    "xg": "indigo",
    "tth": "slategray",
    "other": "blue",
    "tttt_201X": "darkmagenta",
    # "ttt_201X"      : "cornflowerblue",
}

def get_com_args():
    parser = config.get_generic_args()
    parser.add_argument("--drawStyle", type=str, default='stack',
                        help='Way to draw graph',
                        choices=['stack', 'compare', 'sigratio'])
    parser.add_argument("-sig", "--signal", type=str, default='',
                        help="Name of the group to be made into the Signal")
    parser.add_argument("--logy", action='store_true',
                        help="Use logaritmic scale on Y-axis")
    parser.add_argument("--stack_signal", action='store_true',
                        help="Stack signal hists on top of background")
    parser.add_argument("--ratio_range", nargs=2, default=[0.4, 1.6],
                        help="Ratio min ratio max (default 0.5 1.5)")
    parser.add_argument("--no_ratio", action="store_true",
                        help="Do not add ratio comparison")
    return parser.parse_args()

def makePlot(histName, info, basePath, infileName, channels):
    print("Processing {}".format(histName))
    isDcrt = info.isDiscreteGraph(histName)
    inFile = uproot.open(infileName)
    for chan in channels:
        signal = pyHist(info.getLegendName(signalName), color_by_group[signalName], isDcrt)
        ratio = pyHist("Ratio", "black", isDcrt)
        error = pyHist("Stat Errors", "plum", isDcrt)
        band = pyHist("Ratio", "plum", isDcrt)
        data = pyHist("Data", 'black', isDcrt)

        #### FIX
        groupHists = config.getNormedHistos(inFile, info, histName, chan)
        exclude = [signalName, 'data']

        if signalName in groupHists:
            signal.copy_into(groupHists[signalName])
        # data
        if False:
            data.copy_into(groupHists['data']) 
            
        drawOrder = config.getDrawOrder(groupHists, color_by_group, info, ex=exclude)
        stacker = pyStack(drawOrder, isMult=isDcrt)
        stacker.setColors(color_by_group)
        stacker.setLegendNames(info)
        error.copy_into(stacker.getHist())
        if not signal.empty():
            scale = config.findScale(np.sum(stacker.stack) / signal.integral())
            signal.scaleHist(scale)

        # ratio
        if not signal.empty():
            ratio.copy_into(signal.copy().divide(stacker.getHist()))
            ratio.scaleHist(signal.draw_sc)
            band.copy_into(stacker.getHist().copy().divide(stacker.getHist()))

        # Extra options
        stacker.setDrawType(args.drawStyle)

        pad = pyPad(plt, not ratio.empty())

        n, bins, patches = pad().hist(**stacker.getInputs())
        stacker.applyPatches(plt, patches)

        if not signal.empty():
            pad().hist(**signal.getInputsHist())
            pad().errorbar(**signal.getInputs())
        if not data.empty():
            pad().errorbar(**data.getInputs())
        if not error.empty():
            pad().hist(**error.getInputsError())
        if not ratio.empty():
            pad(sub_pad=True).errorbar(**ratio.getInputs())
            pad(sub_pad=True).hist(**band.getInputsError())

        pad.setLegend(info.getPlotSpec(histName))
        pad.axisSetup(info.getPlotSpec(histName), stacker.getRange())
        hep.cms.label(ax=pad(), year="")
        
        fig = plt.gcf()

        if chan == "all" or len(channels) == 1:
            chan = ""
        baseChan = "{}/{}".format(basePath, chan)
        plotBase = "{}/plots/{}".format(baseChan, histName)
        plt.savefig("{}.png".format(plotBase), format="png", bbox_inches='tight')
        plt.savefig("{}.pdf".format(plotBase), format="pdf", bbox_inches='tight')
        plt.close()

        # setup log file
        logger = LogFile(histName, info, "{}/logs".format(baseChan))
        logger.add_metainfo(callTime, command)
        logger.add_mc(drawOrder)
        if not signal.empty():
            logger.add_signal(groupHists[signalName], signalName)
        logger.write_out()


def makePlotStar(args):
    makePlot(*args)



if __name__ == "__main__":
    args = get_com_args()
    callTime = str(datetime.datetime.now())
    command = ' '.join(sys.argv)
    anaSel = args.analysis.split('/')
    if len(anaSel) == 1:
        anaSel.append('')

    info = InfoGetter(anaSel[0], anaSel[1], args.infile, args.info)
    if args.drawStyle == "compare":
        info.setLumi(-1)
    else:
        info.setLumi(args.lumi * 1000)

    info.setDrawStyle(args.drawStyle)
    if not color_by_group:
        config.printDrawObjAndExit(info)

    if args.signal and args.signal not in color_by_group:
        print("signal not in list of groups!")
        print(color_by_group.keys())
        exit(1)
    signalName = args.signal
    channels = args.channels.split(',')

    basePath = config.setupPathAndDir(args.analysis, args.drawStyle, args.path,
                                      channels)

    argList = list()
    for histName in info.getListOfHists():
        if not info.isInPlotSpec(histName):
            continue
        argList.append((histName, info, basePath, args.infile, channels))


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
        writeHTML("{}/{}".format(basePath, chan), "{}/{}".format(args.analysis, chan))
    userName = os.environ['USER']
    htmlPath = basePath[basePath.index(userName) + len(userName) + 1:][4:]
    if 'hep.wisc.edu' in os.environ['HOSTNAME']:
        print("https://www.hep.wisc.edu/~{0}/{1}".format(userName, htmlPath))
    else:
        print("https://{0}.web.cern.ch/{0}/{1}".format(userName, htmlPath))
