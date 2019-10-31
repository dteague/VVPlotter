# -*- coding: utf-8 -*-

info = {
    "GetXaxis.SetTitle" : {
        "HT" :             "H_{T} (GeV)",
        "Met" :            "p_{T}^{miss} (GeV)",
        "centrality":      "Centrality",
        "sphericity" :     "sphericity",
        "nbjet" :          "N_{b}",
        "njet" :           "N_{jets}",
        "nleps" :          "N_{leps}", 
        "ptl1" :           "p_{T}(\ell_{1})\ (GeV)",
        "ptl2" :           "p_{T}(\ell_{2})\ (GeV)",
        "ptj1" :           "p_{T}(j_{1}) (GeV)",
        "ptj2" :           "p_{T}(j_{2}) (GeV)",
        "ptj3" :           "p_{T}(j_{3}) (GeV)",
        "etaj1" :          "#eta(j_{1})",
        "etaj2" :          "#eta(j_{2})",
        "etaj3" :          "#eta(j_{3})",
        "ptb1" :           "p_{T}(b_{1}) (GeV)",
        "ptb2" :           "p_{T}(b_{2}) (GeV)",
        "ptb3" :           "p_{T}(b_{3}) (GeV)",
        "etab1" :          "#eta(b_{1})",
        "etab2" :          "#eta(b_{2})",
        "etab3" :          "#eta(b_{3})",
        "ptj1OverHT" :     "p_{T}(j_{1}) / H_{T}",
        "ptb1OverHT" :     "p_{T}(b_{1}) / H_{T}",
        "dphi_l1j1"  :     "Δφ(ℓ_{1}, j_{1})",
        "dphi_l1j2"  :     "Δφ(ℓ_{1}, j_{2})",
        "dphi_l1j3"  :     "Δφ(ℓ_{1}, j_{3})",
        
    },
    
    "Rebin" : {
        "centrality" : 4,
        "ptl1" : 4,
        "sphericity" : 4,
        "ptj1":   10,
        "ptj2":   10,
        "ptj3":   10,
        "ptb1":   8,
        "ptb2":   8,
        "ptb3":   4,
        "ptj1OverHT" : 4,
        "ptb1OverHT" : 4,
        "dphi_l1j1" : 25,
        "dphi_l1j2" : 25,
        "dphi_l1j3" : 25,
        "etaj1" :     20,
        "etaj2" :     20,
        "etaj3" :     20,
        "etab1" :     20,
        "etab2" :     20,
        "etab3" :     20,
    },
    
    "GetXaxis.SetRangeUser" : {
        "nbjet" : (0, 8),
        "njet" : (0, 12),
        "nleps" : (0, 5),
        "ptl2" :  (0, 200),
        
        "ptj1" :  (0, 800),
        "ptj2" :  (0, 450),
        "ptj3" :  (0, 300),
        "ptb1" :  (0, 600),
        "ptb2" :  (0, 300),
        "ptb3" :  (0, 200),
    }

    
}
