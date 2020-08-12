#!/usr/bin/env python
import sys
import os
import numpy as np
import uproot
import Utilities.configHelper as config
from Utilities.Systematic_Combine import Systematic
from Utilities.InfoGetter import InfoGetter
from histograms.pyUproot import GenericHist
from Utilities.UprootWriter import get_hist

#plot_groups = ["ttt", "tttt", "ttz", "ttw", "tth", "ttXY", "xg", "other", "rare"]
plot_groups = ["ttt", "ttz", "ttw", "tth", "ttXY", "xg", "other", "rare_no3top"]
fitvar = "BDT.Background"
channels = ["SS"]

systematics = [
    ["lumi2016_13TeV", "lnN", [(1.025)]],
        #        ["CMS_norm_tttt", "lnN",  [("tttt", 1.5)]],
#                ["CMS_norm_ttw", "lnN",   [("ttw", 1.4)]],
#                ["CMS_norm_ttz", "lnN",   [("ttz", 1.4)]],
#                ["CMS_norm_tth", "lnN",   [("tth", 1.25)]],
#                ["CMS_norm_xg", "lnN",    [("xg", 1.5)]],
#                ["CMS_norm_rare", "lnN",  [("rare", 1.5)]],
]

# Start of funtions

def get_com_args():
    parser = config.get_generic_args()
    parser.add_argument("-o", "--outdir", type=str, required=True,
                        help="output directory")

    return parser.parse_args()
    

def write_card(outname, fitvar, rate_list, syst_list):
    with open(outname, 'w') as f:
        f.write("imax {}  number of channels\n".format(len(channels)))
        f.write("jmax {}  number of backgrounds plus signals minus 1\n"
                .format(len(plot_groups) - 1))
        f.write("kmax {} number of nuisance parameters (sources of systematical uncertainties)\n"
                .format(len(syst_list)))
        f.write("------------\n\n")

        rootpath = os.path.abspath(outname.replace("card.txt", "hists.root"))
        for group in plot_groups:
            f.write("shapes {0}\t* {1} {0}_{2}_$CHANNEL\t{0}_{2}_$SYSTEMATIC_$CHANNEL\n"
                    .format(group, rootpath, fitvar))

        f.write("\nshapes data_obs\t* {1} {0}_{2}_$CHANNEL\t{0}_{2}_$SYSTEMATIC_$CHANNEL\n\n"
                .format("data", rootpath, fitvar))  # need to create data
        f.write("bin\t\t" + "\t".join(channels))
        f.write("\nobservation\t-1\n\n")
        f.write("------------")
        f.write("""
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin""")

        f.write("\nbin")
        f.write("".join(["\t{}".format(chan)*len(plot_groups) for chan in channels]))
        f.write("\nprocess\t")
        f.write(("\t".join(plot_groups)+"\t")*len(channels))
        f.write("\nprocess\t")
        f.write(("\t".join(np.arange(len(plot_groups)).astype(str))+"\t")*len(channels))
        f.write("\nrate\t" + "\t".join(rate_list.astype(str)))

        f.write("\n" + "-"*80 + "\n")
        for syst in syst_list:
            f.write(syst.output() + "\n")

        f.write("\n* autoMCStats 1")


def main(args):
    anaSel = args.analysis.split('/')
    if len(anaSel) == 1:
        anaSel.append('')
        
    info = InfoGetter(anaSel[0], anaSel[1], args.infile, args.info)
    info.setLumi(args.lumi * 1000)
    
    
    syst_list = list()
    Systematic.groups = plot_groups
    Systematic.chans = channels
    for syst in systematics:
        syst_list.append(Systematic(syst[0], syst[1]))
        syst_list[-1].add_syst_info(syst[2])

    config.checkOrCreateDir(args.outdir)
    outname = "{}/{}_{}_card.txt".format(args.outdir, anaSel[0], fitvar)
    
    
    outFile = uproot.recreate(outname.replace("card.txt", "hists.root"))
    rates = list()
    
    for chan in channels:
        groupHists = config.getNormedHistos(args.infile, info, fitvar, chan)
        groupHists["ttt"].scale(1)
        data = GenericHist()
        for name, hist in groupHists.items():
            if name not in plot_groups:
                continue
            data += hist
        for group in plot_groups:
            rates.append(groupHists[group].integral())
            outFile["{}_{}_{}".format(group, fitvar, chan)] = get_hist(groupHists[group])
        outFile["{}_{}_{}".format("data", fitvar, chan)] = get_hist(data)
    rates = np.array(rates)
    outFile.close()
    
    write_card(outname, fitvar, rates, syst_list)

if __name__ == "__main__":
    args = get_com_args()
    main(args)
