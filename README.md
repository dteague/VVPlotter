TODO: explain style and all the inputs
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

## Colors
### Red
| color | name | hex |
| -- | -- | -- |
|![ff9999](https://placehold.it/25/ff9999/000000?text=+)|`lightsalmon`|`0xff9999`|
|![ff6666](https://placehold.it/25/ff6666/000000?text=+)|`salmon`|`0xff6666`|
|![cc6666](https://placehold.it/25/cc6666/000000?text=+)|`indianred`|`0xcc6666`|
|![cc0033](https://placehold.it/25/cc0033/000000?text=+)|`crimson`|`0xcc0033`|
|![cc3333](https://placehold.it/25/cc3333/000000?text=+)|`firebrick`|`0xcc3333`|
|![ff0000](https://placehold.it/25/ff0000/000000?text=+)|`red`|`0xff0000`|
|![990000](https://placehold.it/25/990000/000000?text=+)|`darkred`|`0x990000`|
|![ff9933](https://placehold.it/25/ff9933/000000?text=+)|`coral`|`0xff9933`|
|![ff6633](https://placehold.it/25/ff6633/000000?text=+)|`tomato`|`0xff6633`|


### orange
| color | name | hex |
| -- | -- | -- |
|![ff3300](https://placehold.it/25/ff3300/000000?text=+)|`orangered`|`0xff3300`|
|![ffcc00](https://placehold.it/25/ffcc00/000000?text=+)|`gold`|`0xffcc00`|
|![ff9900](https://placehold.it/25/ff9900/000000?text=+)|`orange`|`0xff9900`|


### yellow
| color | name | hex |
| -- | -- | -- |
|![ffffcc](https://placehold.it/25/ffffcc/000000?text=+)|`lemonchiffon`|`0xffffcc`|
|![ffff99](https://placehold.it/25/ffff99/000000?text=+)|`khaki`|`0xffff99`|
|![cccc66](https://placehold.it/25/cccc66/000000?text=+)|`darkkhaki`|`0xcccc66`|
|![ffff00](https://placehold.it/25/ffff00/000000?text=+)|`yellow`|`0xffff00`|

### green
| color | name | hex |
| -- | -- | -- |
|![66ff00](https://placehold.it/25/66ff00/000000?text=+)|`lawngreen`|`0x66ff00`|
|![99ff00](https://placehold.it/25/99ff00/000000?text=+)|`chartreuse`|`0x99ff00`|
|![33cc33](https://placehold.it/25/33cc33/000000?text=+)|`limegreen`|`0x33cc33`|
|![00ff00](https://placehold.it/25/00ff00/000000?text=+)|`lime`|`0x00ff00`|
|![339933](https://placehold.it/25/339933/000000?text=+)|`forestgreen`|`0x339933`|
|![009900](https://placehold.it/25/009900/000000?text=+)|`green`|`0x009900`|
|![006600](https://placehold.it/25/006600/000000?text=+)|`darkgreen`|`0x006600`|
|![99ff33](https://placehold.it/25/99ff33/000000?text=+)|`greenyellow`|`0x99ff33`|
|![99cc33](https://placehold.it/25/99cc33/000000?text=+)|`yellowgreen`|`0x99cc33`|
|![00ff66](https://placehold.it/25/00ff66/000000?text=+)|`springgreen`|`0x00ff66`|
|![00ff99](https://placehold.it/25/00ff99/000000?text=+)|`mediumspringgreen`|`0x00ff99`|
|![99ff99](https://placehold.it/25/99ff99/000000?text=+)|`palegreen`|`0x99ff99`|
|![99cc99](https://placehold.it/25/99cc99/000000?text=+)|`darkseagreen`|`0x99cc99`|
|![33cc66](https://placehold.it/25/33cc66/000000?text=+)|`mediumseagreen`|`0x33cc66`|
|![339966](https://placehold.it/25/339966/000000?text=+)|`seagreen`|`0x339966`|
|![999900](https://placehold.it/25/999900/000000?text=+)|`olive`|`0x999900`|
|![666633](https://placehold.it/25/666633/000000?text=+)|`darkolivegreen`|`0x666633`|
|![669933](https://placehold.it/25/669933/000000?text=+)|`olivedrab`|`0x669933`|

### cyan
| color | name | hex |
| -- | -- | -- |
|![ccffff](https://placehold.it/25/ccffff/000000?text=+)|`lightcyan`|`0xccffff`|
|![00ffff](https://placehold.it/25/00ffff/000000?text=+)|`cyan`|`0x00ffff`|
|![66ffcc](https://placehold.it/25/66ffcc/000000?text=+)|`aquamarine`|`0x66ffcc`|
|![66cc99](https://placehold.it/25/66cc99/000000?text=+)|`mediumaquamarine`|`0x66cc99`|
|![99ffff](https://placehold.it/25/99ffff/000000?text=+)|`paleturquoise`|`0x99ffff`|
|![33ffcc](https://placehold.it/25/33ffcc/000000?text=+)|`turquoise`|`0x33ffcc`|
|![33cccc](https://placehold.it/25/33cccc/000000?text=+)|`mediumturquoise`|`0x33cccc`|
|![00cccc](https://placehold.it/25/00cccc/000000?text=+)|`darkturquoise`|`0x00cccc`|
|![339999](https://placehold.it/25/339999/000000?text=+)|`lightseagreen`|`0x339999`|
|![669999](https://placehold.it/25/669999/000000?text=+)|`cadetblue`|`0x669999`|
|![009999](https://placehold.it/25/009999/000000?text=+)|`darkcyan`|`0x009999`|
|![009966](https://placehold.it/25/009966/000000?text=+)|`teal`|`0x009966`|


### blue
| color | name | hex |
| -- | -- | -- |
|![99ccff](https://placehold.it/25/99ccff/000000?text=+)|`lightskyblue`|`0x99ccff`|
|![00ccff](https://placehold.it/25/00ccff/000000?text=+)|`deepskyblue`|`0x00ccff`|
|![99cccc](https://placehold.it/25/99cccc/000000?text=+)|`lightsteelblue`|`0x99cccc`|
|![3399ff](https://placehold.it/25/3399ff/000000?text=+)|`dodgerblue`|`0x3399ff`|
|![6699ff](https://placehold.it/25/6699ff/000000?text=+)|`cornflowerblue`|`0x6699ff`|
|![3399cc](https://placehold.it/25/3399cc/000000?text=+)|`steelblue`|`0x3399cc`|
|![3366cc](https://placehold.it/25/3366cc/000000?text=+)|`royalblue`|`0x3366cc`|
|![0000ff](https://placehold.it/25/0000ff/000000?text=+)|`blue`|`0x0000ff`|
|![0000cc](https://placehold.it/25/0000cc/000000?text=+)|`mediumblue`|`0x0000cc`|
|![000099](https://placehold.it/25/000099/000000?text=+)|`darkblue`|`0x000099`|
|![000066](https://placehold.it/25/000066/000000?text=+)|`navy`|`0x000066`|
|![003366](https://placehold.it/25/003366/000000?text=+)|`midnightblue`|`0x003366`|
|![6666ff](https://placehold.it/25/6666ff/000000?text=+)|`mediumslateblue`|`0x6666ff`|
|![6666cc](https://placehold.it/25/6666cc/000000?text=+)|`slateblue`|`0x6666cc`|
|![333399](https://placehold.it/25/333399/000000?text=+)|`darkslateblue`|`0x333399`|

### purple
| color | name | hex |
| -- | -- | -- |
|![ffccff](https://placehold.it/25/ffccff/000000?text=+)|`lavender`|`0xffccff`|
|![cc99cc](https://placehold.it/25/cc99cc/000000?text=+)|`plum`|`0xcc99cc`|
|![ff99ff](https://placehold.it/25/ff99ff/000000?text=+)|`violet`|`0xff99ff`|
|![cc66cc](https://placehold.it/25/cc66cc/000000?text=+)|`orchid`|`0xcc66cc`|
|![ff00ff](https://placehold.it/25/ff00ff/000000?text=+)|`magenta`|`0xff00ff`|
|![cc33cc](https://placehold.it/25/cc33cc/000000?text=+)|`mediumorchid`|`0xcc33cc`|
|![9966cc](https://placehold.it/25/9966cc/000000?text=+)|`mediumpurple`|`0x9966cc`|
|![9933ff](https://placehold.it/25/9933ff/000000?text=+)|`blueviolet`|`0x9933ff`|
|![9900cc](https://placehold.it/25/9900cc/000000?text=+)|`darkviolet`|`0x9900cc`|
|![9933cc](https://placehold.it/25/9933cc/000000?text=+)|`darkorchid`|`0x9933cc`|
|![990099](https://placehold.it/25/990099/000000?text=+)|`darkmagenta`|`0x990099`|
|![990066](https://placehold.it/25/990066/000000?text=+)|`purple`|`0x990066`|
|![660099](https://placehold.it/25/660099/000000?text=+)|`indigo`|`0x660099`|


### pink
| color | name | hex |
| -- | -- | -- |
|![ffcccc](https://placehold.it/25/ffcccc/000000?text=+)|`pink`|`0xffcccc`|
|![ff99cc](https://placehold.it/25/ff99cc/000000?text=+)|`lightpink`|`0xff99cc`|
|![ff66cc](https://placehold.it/25/ff66cc/000000?text=+)|`hotpink`|`0xff66cc`|
|![ff0099](https://placehold.it/25/ff0099/000000?text=+)|`deeppink`|`0xff0099`|
|![cc6699](https://placehold.it/25/cc6699/000000?text=+)|`palevioletred`|`0xcc6699`|
|![cc3399](https://placehold.it/25/cc3399/000000?text=+)|`mediumvioletred`|`0xcc3399`|


### white/grey/black
| color | name | hex |
| -- | -- | -- |
|![ffffff](https://placehold.it/25/ffffff/000000?text=+)|`white`|`0xffffff`|
|![cccccc](https://placehold.it/25/cccccc/000000?text=+)|`lightgray`|`0xcccccc`|
|![999999](https://placehold.it/25/999999/000000?text=+)|`darkgray`|`0x999999`|
|![666666](https://placehold.it/25/666666/000000?text=+)|`dimgray`|`0x666666`|
|![666699](https://placehold.it/25/666699/000000?text=+)|`slategray`|`0x666699`|
|![336666](https://placehold.it/25/336666/000000?text=+)|`darkslategray`|`0x336666`|
|![000000](https://placehold.it/25/000000/000000?text=+)|`black`|`0x000000`|

### brown
| color | name | hex |
| -- | -- | -- |
|![ffcc99](https://placehold.it/25/ffcc99/000000?text=+)|`navajowhite`|`0xffcc99`|
|![cccc99](https://placehold.it/25/cccc99/000000?text=+)|`tan`|`0xcccc99`|
|![cc9999](https://placehold.it/25/cc9999/000000?text=+)|`rosybrown`|`0xcc9999`|
|![ff9966](https://placehold.it/25/ff9966/000000?text=+)|`sandybrown`|`0xff9966`|
|![cc9900](https://placehold.it/25/cc9900/000000?text=+)|`goldenrod`|`0xcc9900`|
|![cc9933](https://placehold.it/25/cc9933/000000?text=+)|`peru`|`0xcc9933`|
|![cc6633](https://placehold.it/25/cc6633/000000?text=+)|`chocolate`|`0xcc6633`|
|![993300](https://placehold.it/25/993300/000000?text=+)|`saddlebrown`|`0x993300`|
|![996633](https://placehold.it/25/996633/000000?text=+)|`sienna`|`0x996633`|
|![993333](https://placehold.it/25/993333/000000?text=+)|`brown`|`0x993333`|
|![660000](https://placehold.it/25/660000/000000?text=+)|`maroon`|`0x660000`|
