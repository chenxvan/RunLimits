#!/usr/bin/env python
import ROOT
#from ROOT import ROOT, TCanvas, TGraph, TGraphAsymmErrors, TPaveText, TColor
from ROOT import TGraph, TGraphAsymmErrors, TCanvas, TGraph, TGraphAsymmErrors, TPaveText, TColor
ROOT.gROOT.SetBatch()
label_TL = '#font[62]{CMS}'

class parameter:
    def __init__(self, name, value, error):
        self.name = name
        self.value = value
        self.error = error

def get_parameters_from_file(input_file_):

    par_list = []

    f = open(input_file_,'r')
    for line in f:
        vals = line.split(None, 2)
        if len(vals) != 3:
            print '\n@@@ FATAL -- uncorrect input file format. stopping script. ('+input_file_+')\n'
            raise SystemExit

        value = float(vals[0])
        error = float(vals[1])
        name = str(vals[2])

        par_list.append(parameter(name, value, error))

    return par_list

def nuisance_plot(input_file_, orien_, sticker_, oname_):

    pars = get_parameters_from_file(input_file_)
    #adjust_parameters(pars)

    N = len(pars)
    print N
    g68 = TGraph(2*N+7)
    g95 = TGraph(2*N+7)
    gPR = TGraphAsymmErrors(N)

    for i in range(0,N):
        x = pars[i].value
        y = i + 1.5
        xerr = pars[i].error
        yerr = 0.

        if orien_ == 'h':
            x, y = y, x
            xerr, yerr = yerr, xerr

        gPR.SetPoint(i, x, y);
        gPR.SetPointEXlow(i, xerr);
        gPR.SetPointEYlow(i, yerr);
        gPR.SetPointEXhigh(i, xerr);
        gPR.SetPointEYhigh(i, yerr);

    for a in range(0,N+3):

        if orien_ == 'h':
            g68.SetPoint(a, a, -1)
            g95.SetPoint(a, a, -2)
            g68.SetPoint(a+1+N+2, N+2-a, 1)
            g95.SetPoint(a+1+N+2, N+2-a, 2)

        else:
            g68.SetPoint(a,-1, a)
            g95.SetPoint(a,-2, a)
            g68.SetPoint(a+1+N+2,1, N+2-a)
            g95.SetPoint(a+1+N+2,2, N+2-a)

    gPR.SetLineStyle(1);
    gPR.SetLineWidth(1);
    gPR.SetLineColor(1);
    gPR.SetMarkerStyle(21);
    gPR.SetMarkerSize(1.25);

    g68.SetFillColor(ROOT.kGreen);
#    g68.SetFillColor(ROOT.gROOT.GetColor(kGreen));
    g95.SetFillColor(ROOT.kYellow);

    if orien_ == 'h':
        text_TL = TPaveText(0.100, 0.925, 0.440, 0.995, 'NDC')
        text_TR = TPaveText(0.587, 0.925, 0.999, 0.993, 'NDC')

    else:
        text_TL = TPaveText(0.370, 0.945, 0.590, 0.995, 'NDC')
        text_TR = TPaveText(0.600, 0.945, 0.995, 0.993, 'NDC')

    text_TL.AddText(label_TL)
    text_TL.SetFillColor(0)
    text_TL.SetTextAlign(12)
    text_TL.SetTextSize(0.06)
    text_TL.SetTextFont(42)

    text_TR.AddText(sticker_)
    text_TR.SetFillColor(0)
    text_TR.SetTextAlign(32)
    text_TR.SetTextSize(0.05)
    text_TR.SetTextFont(42)

    if orien_ == 'h':
        c = TCanvas('c','c',1000,700)
        c.SetTopMargin(0.08)
        c.SetRightMargin(0.02)
        c.SetBottomMargin(0.16)
        c.SetLeftMargin(0.11)

    else:
        c = TCanvas('c','c',700,1000)
        c.SetTopMargin(0.06)
        c.SetRightMargin(0.02)
        c.SetBottomMargin(0.12)
        c.SetLeftMargin(0.35*700/650)

    c.SetTickx()
    c.SetTicky()

    c.Update()
    g95.Draw('AF')
    g68.Draw('F')
    gPR.Draw('P')
    text_TL.Draw('same')
    text_TR.Draw('same')

    ax_1 = g95.GetHistogram().GetYaxis();
    ax_2 = g95.GetHistogram().GetXaxis();
    if orien_ == 'h': ax_1, ax_2 = ax_2, ax_1

    ax_1.Set(N+2,0,N+2);
    ax_1.SetNdivisions(-414);
    for i in range(0,N): ax_1.SetBinLabel(i+2, pars[i].name);

    g95.SetTitle('')
#    ax_2.SetRangeUser(-4.4, 4.4)
    ax_2.SetTitle('post-fit nuisance parameters values')
    #ax_2.SetTitle('deviation in units of #sigma')
    ax_1.SetTitleSize(0.050)
    ax_2.SetTitleSize(0.050)
    ax_1.SetTitleOffset(1.4)
    ax_2.SetTitleOffset(1.0)
    ax_1.SetLabelSize(0.05)
    #ax_2.SetLabelSize(0.05)
    ax_1.SetRangeUser(0, N+2)
    ax_2.SetRangeUser(-2.4, 2.4)
    g95.GetHistogram().Draw('axis,same')
    c.SaveAs(oname_+'.pdf')

    c.Close()

###


#input_file = '/nfs/dust/cms/user/karavdia/ttbar_semilep_13TeV/RunII_80X_v1/ttbarLJAnalysis/Selas2015_13fb_playLimits_20160801/lep/mle_fit.txt'
#input_file = '/nfs/dust/cms/user/karavdia/ttbar_semilep_13TeV/RunII_80X_v2/ttbarLJAnalysis/Selas2015_12fb_271036_284044_JSON_Mtt_shrink_Leppt60_Jetpt180_METcorrect/elec/mle_fit.txt'
#input_file = '/nfs/dust/cms/user/karavdia/ttbar_semilep_13TeV/RunII_80X_v3/ttbarLJAnalysis/MLEtest_ElecID_MVA_loose_MET50_elecPt50_EGReg_jetIDtight_slimmedMETsMuEGClean/mle_fit.txt'
#input_file = '/nfs/dust/cms/user/karavdia/ttbar_semilep_13TeV/RunII_80X_v3/ttbarLJAnalysis/ElecID_MVA_tight_MET50_elecPt50_EGReg_jetIDtight_slimmedMETs_JLCdR_BLINDED_HLT1ORHLT2_wBtagSFs_jet2pt50/T1_v06/mle_fit.txt'
input_file = 'mle_fit.txt'
nuisance_plot(input_file, 'v', 'background-only', 'mle_nosig')
