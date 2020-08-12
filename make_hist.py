#!/usr/bin/env python
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import subprocess
import matplotlib.pyplot as plt
import mplhep as hep
import datetime
import sys
import multiprocessing as mp
import logging

from Utilities.InfoGetter import InfoGetter
from histograms import *
from Utilities.LogFile import LogFile
from Utilities.makeSimpleHtml import writeHTML
import Utilities.configHelper as config

plt.style.use([hep.style.CMS, hep.style.firamath])
logging.getLogger('matplotlib.font_manager').disabled = True

color_by_group = {
    "ttt": "crimson",
    "ttz": "mediumseagreen",
    "ttw": "darkgreen",
    "rare_no3top": "darkorange",
    "ttXY": "cornflowerblue",
    "xg": "indigo",
    "tth": "slategray",
    "other": "blue",
    "tttt_201X": "darkmagenta",
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

    for chan in channels:
        signals = {sig: pyHist(info.getLegendName(sig), color_by_group[sig], isDcrt)
                  for sig in signalNames}
        ratio = pyHist("Ratio", "black", isDcrt)
        band = pyHist("Ratio", "plum", isDcrt)

        error = pyHist("Stat Errors", "plum", isDcrt)
        data = pyHist("Data", 'black', isDcrt)

        #### FIX
        groupHists = config.getNormedHistos(infileName, info, histName, chan)
        exclude = ['data', *signalNames]

        for sig in signalNames:
            if sig in groupHists:
                signals[sig].copy_into(groupHists[sig])
        # data
        if False:
            data.copy_into(groupHists['data']) 
            
        drawOrder = config.getDrawOrder(groupHists, color_by_group, info, ex=exclude)
        stacker = pyStack(drawOrder, isMult=isDcrt)
        stacker.setColors(color_by_group)
        stacker.setLegendNames(info)
        error.copy_into(stacker.getHist())
        for sig, signal in signals.items():
            if not signal.empty():
                scale = config.findScale(np.sum(stacker.stack) / signal.integral())
                signals[sig].scaleHist(scale)

        # # ratio
        # if not signal.empty():
        #     ratio.copy_into(signal.copy().divide(stacker.getHist()))
        #     ratio.scaleHist(signal.draw_sc)
        #     band.copy_into(stacker.getHist().copy().divide(stacker.getHist()))

        # Extra options
        stacker.setDrawType(args.drawStyle)

        pad = pyPad(plt, not ratio.empty())

        n, bins, patches = pad().hist(**stacker.getInputs())
        stacker.applyPatches(plt, patches)

        for sig, signal in signals.items():
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
        hep.cms.label(ax=pad(), year="Run II", data=not data.empty()) # , lumi=info.getLumi()/1000

        fig = plt.gcf()

        if chan == "all" or len(channels) == 1:
            chan = ""
        baseChan = "{}/{}".format(basePath, chan)
        plotBase = "{}/plots/{}".format(baseChan, histName)
        plt.savefig("{}.png".format(plotBase), format="png", bbox_inches='tight')
        subprocess.call('convert {0}.png -quality 0 {0}.pdf'.format(plotBase),
                        shell=True)
        plt.close()

        # setup log file
        logger = LogFile(histName, info, "{}/logs".format(baseChan))
        logger.add_metainfo(callTime, command)
        logger.add_mc(drawOrder)
        for sig, signal in signals.items():
            if not signal.empty():
                logger.add_signal(groupHists[sig], sig)
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

    signalNames = args.signal.split(',')
    if not set(signalNames) & set(color_by_group.keys()):
        print("signal not in list of groups!")
        print(color_by_group.keys())
        exit(1)
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

    if 'hep.wisc.edu' in os.environ['HOSTNAME']:
        htmlPath = basePath[basePath.index(userName) + len(userName) + 1:][4:]
        print("https://www.hep.wisc.edu/~{0}/{1}".format(userName, htmlPath))
    else:
        htmlPath = basePath[basePath.index(userName) + len(userName) + 1:][4:]
        print("https://{0}.web.cern.ch/{0}/{1}".format(userName, htmlPath))
