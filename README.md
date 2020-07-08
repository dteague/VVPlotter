VVPlotter: Code base for Plotting and Create Combine related objects from teh VVAnalysis package

[![CircleCI](https://circleci.com/gh/dteague/VVPlotter.svg?style=shield)](https://app.circleci.com/pipelines/github/dteague/VVPlotter)

# Table of Contents
   * [Table of Contents](#table-of-contents)
   * [Styles](#styles)
      * [Colors](#colors)
         * [Red](#red)
         * [orange](#orange)
         * [yellow](#yellow)
         * [green](#green)
         * [cyan](#cyan)
         * [blue](#blue)
         * [purple](#purple)
         * [pink](#pink)
         * [white/grey/black](#whitegreyblack)
         * [brown](#brown)
			 
# How to Run

This repo uses argparse so to see all options, just run `./make_hist.py --help`

The required options are `-i` and `-a` for input and analysis respectively.

- `-s` [Selection]: is not required because defaults to finding `PlotObject` info from the `PlotObject/<Analysi>.json` file. Specify Selection to pick a selection specific histogram
- `l` [Luminosity]: This defaults to -1 or all samples are unit normalization. Give in pb-1
- `c` [Channel]: Default is "all" (actual word "all"), but can change this
- `sig` [Signal]: choose which sample to make your signal

The Samples that will be made into the graph are specified in the `drawObj` array in the `make_hist.py` code. This must be changed to the samples you want.

```
./make_hist.py -i 4top_files.root -a ThreeLep -l 35.9 -o outie.root -sig '2016' --no_ratio
```


# Styles
All of the information for the style is in the `StyleHelper.py` file. The StyleHelper does 2 main things:
1. Give style to the bars in the stack plot
1. Give root attributes to different objects

For the giving style, this is done with PlotGroup file in the ADM. The actual string that is used to give the style is the Style string in the py file and it is blocked into 3 compontents:

1. Describe the fill type of the stack [fill, nofill, hatched]
1. Describe the color of the stack and line (described in full in the color section)
1. Describe the line type [thick, dotdash, dash, largedash, finedash] default is leaving black

This style string has these 3 components put into a string with each component seperated by a dash or:

`fill-red`

`nofill-springgreen-dotdash`

etc.

The Second part of the code is to give a certain object some formatting based on root commands, such as `hist.GetXaxis().SetTitle("blah")`. This is done by putting the command in the `Attributes` section of the `style.py` file in this repo for a given object. The command can be a chained together. Examples are:

`"GetXaxis.SetTitle" : "Hello"`

`"GetXaxis().SetTitleOffset" : 1.3`

