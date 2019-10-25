import ROOT as r

def setStyle(hist, styleStr):
    # stylers (may put in different place)
    extraStyles = {
        "default" : [1, 1], "thick" : [1, 3],
        "dotdash" : [8, 3], "dash" : [7, 3], "largedash" : [9, 2], "finedash" : [3, 3], 
        }
    fillStyles = {"fill" : 1001, "nofill" : 0, "hatch" : 3013}
    from colors import colors
    
    styleBits = styleStr.split('-')
    fillStyle = fillStyles[styleBits.pop(0)]
    color = colors[styleBits.pop(0)]
    lineColor = getLineColor(color)
    extraStyle = extraStyles['default']
    try:
        extraStyle = extraStyles[styleBits.pop(0)]
    except:
        pass
    if fillStyle == 0:
        lineColor = color

    hist.SetFillColor(r.TColor.GetColor('#%06x' % color))
    hist.SetLineColor(r.TColor.GetColor('#%06x' % lineColor))
    hist.SetFillStyle(fillStyle)
    hist.SetLineStyle(extraStyle[0])
    hist.SetLineWidth(extraStyle[1])
    hist.SetMarkerSize(0)
    
def getLineColor(fillColor):
    r = fillColor/0x10000
    g = (fillColor % 0x10000)/0x100
    b = fillColor % 0x100
    sft = 102
    rmod = r - sft if r > sft else 0
    gmod = g - sft if g > sft else 0
    bmod = b - sft if b > sft else 0
    
    return rmod*0x10000 + gmod*0x100 + bmod

def setAttributes(obj, attributes, isStack=False):
    for func, val in attributes.iteritems():
        if isStack and "Get" in func:
            runModule(obj.GetHistogram(), func, val)
        else:
            runModule(obj, func, val)

def runModule(module, func, val):
    funcList = func.split('.')
    tmp = getattr(module, funcList.pop(0).strip("()"))
    for extraFunc in funcList:
        try:
            tmp = getattr(tmp(), extraFunc.strip("()"))
        except:
            tmp = getattr(tmp, extraFunc.strip("()"))
    tmp(val)
    
