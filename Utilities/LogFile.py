from prettytable import PrettyTable
import math
import numpy as np

from Utilities.pyUproot import GenericHist

BKG = 0
SIGNAL = 1
DATA = 2
TOTAL = 3

class LogFile:
    """Wrapper for Logfile for a plot

    Attributes
    ----------
    plotTable : PrettyTable
        PrettyTable holding all the histogram information
    output_name : string
        Name/path of logfile to be created
    analysis : string
        Analysis running over
    selection : string
        Selection of analysis running over
    lumi : float
        Luminosity of this run (in ipb, but converted to ifb in class)
    hists : list of GenericHists
        List of GenericHists indexed by the constants BKG, SIGNAL, DATA, TOTAL
    callTime : string
        String of the time this script was called (any format)
    command : string
        Command used to start this script
    name : string
        Name of the histogram
    
    """
    def __init__(self, name, info, path='.'):
        self.plotTable = PrettyTable(["Plot Group", "Weighted Events", "Error"])
        self.output_name = "{}/{}_info.log".format(path, name)
        self.analysis = info.getAnalysis()
        self.selection = info.getSelection()
        self.lumi = info.getLumi() / 1000
        self.hists = [GenericHist()] * 4
        self.callTime = ""
        self.command = ""
        self.name = name

    def add_mc(self, drawOrder):
        """Add background data to this class

        Parameters
        ----------
        drawOrder : list of tuples (string, GenericHist)
            List of all background hists with their names
        """
        for name, hist in drawOrder:
            self.plotTable.add_row([name, *self.get_int_err(hist)])
            self.hists[BKG] += hist
        self.hists[TOTAL] += self.hists[BKG]

    def add_signal(self, signal, groupName):
        """Add signal data to this class

        Parameters
        ----------
        signal : GenericHist
            Histogram of signal information
        groupName : string
            Name used to label the singal
        """
        self.hists[SIGNAL] += signal
        self.plotTable.add_row([groupName, *self.get_int_err(signal)])
        self.hists[TOTAL] += signal

    def add_metainfo(self, callTime, command):
        """Set specific metadata for output file

        Parameters
        ----------
        callTime : string
            Time script was call (not formated, must be done before here)
        command : string
            Full commandline string use for this run

        """
        self.callTime = callTime
        self.command = command

    def get_int_err(self, hist):
        """Grab the Integral and error on that information

        Parameters
        ----------
        hist : GenericHist or int
            Histogram to get info from or int pointed to self.hists list
        """
        if isinstance(hist, int):
            hist = self.hists[hist]
        return hist.get_int_err()

    def write_out(self, isLatex=False):
        """Write out all current information to the objects output file

        Parameters
        ----------
        isLatex : bool, optional
            Whether table should be written out in latex or org style table
        """
        with open(self.output_name, 'w') as out:
            out.write('-' * 80 + '\n')
            out.write("Script called at {} \n".format(self.callTime))
            out.write("The command was: {} \n".format{self.command})
            out.write("The name of this Histogram is: {} \n"
                         .format(self.name))
            out.write('-' * 80 + '\n')
            out.write("Selection: {}/{}\n".format(self.analysis,
                                                     self.selection))
            out.write("Luminosity: {:0.2f} fb^{{-1}}\n"
                         .format(self.lumi))
            if isLatex:
                out.write('\n' + self.plotTable.get_latex_string() + '\n'*2)
            else:
                out.write('\n' + self.plotTable.get_string() + '\n'*2)

            if not self.hists[TOTAL].empty():
                out.write("Total sum of Monte Carlo: {:0.2f} +/- {:0.2f} \n"
                             .format(*self.get_int_err(TOTAL)))
            if not self.hists[SIGNAL].empty():
                out.write(
                    "Total sum of background Monte Carlo: {:0.2f} +/- {:0.2f} \n"
                    .format(*self.get_int_err(BKG)))
                out.write("Ratio S/(S+B): {:0.2f} +/- {:0.2f} \n"
                          .format(*self.get_sig_bkg_ratio()))
                out.write("Ratio S/sqrt(S+B): {0.2f} +/- {:0.2f} \n"
                          .format(*selfelf.get_likelihood()))
            if not self.hists[DATA].empty():
                out.write("Number of events in data {} \n"
                          .format(*self.get_int_err(DATA)[0]))

    def get_sig_bkg_ratio(self):
        """Get S/B

        Returns
        -------
        tuple
            tuple S/B and its error
        """
        sig, sigErr = self.get_int_err(SIGNAL)
        tot, totErr = self.get_int_err(TOTAL)
        sigbkgd = sig / tot
        sigbkgdErr = sigbkgd * math.sqrt((sigErr / sig)**2 + (totErr / tot)**2)
        return (sigbkgd, sigbkgdErr)

    def get_likelihood(self):
        """Get Figure of merit

        Returns
        -------
        tuple
            tuple Figure of Merit (S/sqrt(S+B)) and its error
        """
        sig, sigErr = self.get_int_err(SIGNAL)
        tot, totErr = self.get_int_err(TOTAL)
        likelihood = sig / math.sqrt(tot)
        likelihoodErr = likelihood * math.sqrt((sigErr / sig)**2 +
                                               (0.5 * totErr / tot)**2)
        return (likelihood, likelihoodErr)
