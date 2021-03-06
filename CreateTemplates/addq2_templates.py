#! /usr/bin/env python
# add "envelope" of q2 variations for ttbar and w+jets
# input: root file with rebinned Mttbar templates 
# output: root file with rebinned Mttbar templates + q2ttbar and q2w+jets variations with name "input name"+_addedQ2.root
# created on 02.11.2017

import sys
sys.argv.append('-b')

import ROOT
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(000000000)
ROOT.gStyle.SetOptTitle(0)

from ROOT import TCanvas, TFile, TH1, THStack, TLegend

class hinfo:
  def __init__(self, name):
    fields = name.split('__')
    self.channel = fields[0]
    self.process = fields[1]
    self.systematic = None
    self.shift = None
    if len(fields) > 2:
      self.systematic = fields[2]
      self.shift = fields[3]


def name(channel, process, systematic = None, shift = None):
  if not systematic:
    return '__'.join([channel, process])
  return '__'.join([channel, process, systematic, shift])



def addq2File(rerror, filename, xtitle, backgrounds):
  file = TFile(filename)
  keys = file.GetListOfKeys()
  h_bkg = {}
  
  system_q2ttbar_list={"q2ttbarMuRdnMuFdn","q2ttbarMuRupMuFup","q2ttbarMuRdnMuFct","q2ttbarMuRupMuFct","q2ttbarMuRctMuFdn","q2ttbarMuRctMuFup"}
  h_tmp_q2syst_q2ttbar = {}
  h_q2syst_q2ttbar = {} # final "q2ttbar__plus","q2ttbar__minus" hists
  
  system_q2wjets_list={"q2wjetsMuRdnMuFdn","q2wjetsMuRupMuFup","q2wjetsMuRdnMuFct","q2wjetsMuRupMuFct","q2wjetsMuRctMuFdn","q2wjetsMuRctMuFup"}
  h_tmp_q2syst_q2wjets = {}
  h_q2syst_q2wjets = {} # final "q2wjets__plus","q2wjets__minus" hists
  
  # load all the background histograms and create tmp hists to store q2 variations
  for key in keys:
    key = key.GetName()
    info = hinfo(key)
    if not info.systematic:
      h_bkg[info.channel+info.process] = file.Get(key).Clone()
      for i in range(1,h_bkg[info.channel+info.process].GetNbinsX()+1):
        h_tmp_q2syst_q2ttbar[info.channel+info.process+str(i)] = ROOT.TH1F(info.channel+info.process+"_"+str(i)+"_q2ttbar",info.channel+info.process+"_"+str(i)+"_q2ttbar", 80000, 0., 20000.)
        h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)] = ROOT.TH1F(info.channel+info.process+"_"+str(i)+"_q2wjets",info.channel+info.process+"_"+str(i)+"_q2wjets", 80000, 0., 20000.)
        
  #read 6 variations for q2ttbar and store them in a histogram. One histtogram per Mttbar bin        
  for key in keys:
    key = key.GetName()
    info = hinfo(key)
    if info.systematic:
      if info.shift == "plus": # plus and minus are identical
        if info.process in backgrounds:
          for key_q2syst_q2ttbar in system_q2ttbar_list:
            if key_q2syst_q2ttbar == info.systematic:
              h_bkg[info.channel+info.process+key_q2syst_q2ttbar] = file.Get(key).Clone()
              for i in range(1,h_bkg[info.channel+info.process+key_q2syst_q2ttbar].GetNbinsX()+1):
                value = h_bkg[info.channel+info.process+key_q2syst_q2ttbar].GetBinContent(i)
                h_tmp_q2syst_q2ttbar[info.channel+info.process+str(i)].Fill(value)

  #read 6 variations for q2wjets and store them in a histogram. One histtogram per Mttbar bin        
  for key in keys:
    key = key.GetName()
    info = hinfo(key)
    if info.systematic:
      if info.shift == "plus": # plus and minus are identical
        if info.process in backgrounds:
          for key_q2syst_q2wjets in system_q2wjets_list:
            if key_q2syst_q2wjets == info.systematic:
              h_bkg[info.channel+info.process+key_q2syst_q2wjets] = file.Get(key).Clone()
              for i in range(1,h_bkg[info.channel+info.process+key_q2syst_q2wjets].GetNbinsX()+1):
                value = h_bkg[info.channel+info.process+key_q2syst_q2wjets].GetBinContent(i)
                h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].Fill(value)

  #store hists in a root file
  output = TFile(filename.split('.')[0]+'_addedQ2.root', 'RECREATE')

  #In each Mttbar bin store Mean-Sigma (minus) and Mean+Sigma(plus) of histogram with 6 q2ttbar variation.
  #This gives "envelope" of q2 variations for ttbar
  #Draw tmp hist for a sanity check and store it in the output root file
  for key in keys:
    key = key.GetName()
    info = hinfo(key)
    if info.systematic:
      if info.process in backgrounds:
        if info.systematic == "q2ttbarMuRdnMuFdn":
          if info.shift == "plus":
            h_q2syst_q2ttbar["q2ttbar__plus"+info.channel] = h_bkg[info.channel+info.process+info.systematic].Clone()
            h_q2syst_q2ttbar["q2ttbar__plus"+info.channel].SetName(info.channel+"__ttbar"+"__q2ttbar__plus")
            h_q2syst_q2ttbar["q2ttbar__plus"+info.channel].SetTitle(info.channel+"__ttbar"+"__q2ttbar__plus")
            h_q2syst_q2ttbar["q2ttbar__minus"+info.channel] = h_bkg[info.channel+info.process+info.systematic].Clone()
            h_q2syst_q2ttbar["q2ttbar__minus"+info.channel].SetName(info.channel+"__ttbar"+"__q2ttbar__minus")
            h_q2syst_q2ttbar["q2ttbar__minus"+info.channel].SetTitle(info.channel+"__ttbar"+"__q2ttbar__minus")

            canvas = TCanvas()
            for i in range(1,h_bkg[info.channel+info.process+info.systematic].GetNbinsX()+1):
              h_q2syst_q2ttbar["q2ttbar__plus"+info.channel].SetBinContent(i,h_tmp_q2syst_q2ttbar[info.channel+info.process+str(i)].GetMean()+h_tmp_q2syst_q2ttbar[info.channel+info.process+str(i)].GetRMS())
              h_q2syst_q2ttbar["q2ttbar__minus"+info.channel].SetBinContent(i,h_tmp_q2syst_q2ttbar[info.channel+info.process+str(i)].GetMean()-h_tmp_q2syst_q2ttbar[info.channel+info.process+str(i)].GetRMS())
               
            #plots hists for canity check  
            h_q2syst_q2ttbar["q2ttbar__plus"+info.channel].SetLineColor(2)
            h_q2syst_q2ttbar["q2ttbar__minus"+info.channel].SetLineColor(3)                  
            h_q2syst_q2ttbar["q2ttbar__plus"+info.channel].Draw('hist')
            h_q2syst_q2ttbar["q2ttbar__minus"+info.channel].Draw('samehist')
            canvas.SaveAs(info.channel+'__'+info.process+'__q2ttbar.pdf')
            output.cd()
            h_q2syst_q2ttbar["q2ttbar__minus"+info.channel].Write()
            h_q2syst_q2ttbar["q2ttbar__plus"+info.channel].Write()

  #In each Mttbar bin store Mean-Sigma (minus) and Mean+Sigma(plus) of histogram with 6 q2wjets variation.
  #This gives "envelope" of q2 variations for w+jets
  #Draw tmp hist for a sanity check and store it in the output root file
  for key in keys:
    key = key.GetName()
    info = hinfo(key)
    if info.systematic:
      if info.process in backgrounds:
        if info.systematic == "q2wjetsMuRdnMuFdn":
          if info.shift == "plus":
            h_q2syst_q2wjets["q2wjets__plus"+info.channel] = h_bkg[info.channel+info.process+info.systematic].Clone()
            h_q2syst_q2wjets["q2wjets__plus"+info.channel].SetName(info.channel+"__wjets_l"+"__q2wjets__plus")
            h_q2syst_q2wjets["q2wjets__plus"+info.channel].SetTitle(info.channel+"__wjets_l"+"__q2wjets__plus")
            h_q2syst_q2wjets["q2wjets__minus"+info.channel] = h_bkg[info.channel+info.process+info.systematic].Clone()
            h_q2syst_q2wjets["q2wjets__minus"+info.channel].SetName(info.channel+"__wjets_l"+"__q2wjets__minus")
            h_q2syst_q2wjets["q2wjets__minus"+info.channel].SetTitle(info.channel+"__wjets_l"+"__q2wjets__minus")
            canvas = TCanvas()
            for i in range(1,h_bkg[info.channel+info.process+info.systematic].GetNbinsX()+1):
              #print i, h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].GetMean(), h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].GetRMS()
              h_q2syst_q2wjets["q2wjets__plus"+info.channel].SetBinContent(i,h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].GetMean()+h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].GetRMS())
              h_q2syst_q2wjets["q2wjets__minus"+info.channel].SetBinContent(i,h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].GetMean()-h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].GetRMS())
              # canvasTMP = TCanvas()
              # h_tmp_q2syst_q2wjets[info.channel+info.process+str(i)].Draw('hist')
              # canvasTMP.SaveAs(info.channel+info.process+str(i)+'.pdf')
                            
            #plots hists for canity check  
            h_q2syst_q2wjets["q2wjets__plus"+info.channel].SetLineColor(2)
            h_q2syst_q2wjets["q2wjets__minus"+info.channel].SetLineColor(3)                  
            h_q2syst_q2wjets["q2wjets__plus"+info.channel].Draw('hist')
            h_q2syst_q2wjets["q2wjets__minus"+info.channel].Draw('samehist')
            canvas.SaveAs(info.channel+'__'+info.process+'__q2wjets.pdf')
                                    
            output.cd()
            h_q2syst_q2wjets["q2wjets__minus"+info.channel].Write()
            h_q2syst_q2wjets["q2wjets__plus"+info.channel].Write()

  #Add the rest of systematic to the new root file
  system_q2_list = system_q2ttbar_list
  system_q2_list.update(system_q2wjets_list)
  h_all_system = {}
  for key in keys:
    key = key.GetName()
    #print key
    info = hinfo(key)
    if not info.systematic:
      h_all_system[info.channel+"__"+info.process] = file.Get(key).Clone()
      output.cd()
      h_all_system[info.channel+"__"+info.process].Write()
       
    if info.systematic:
      isStore = True
      for key_q2_q2wjets in system_q2_list:
        if info.systematic == key_q2_q2wjets:
          isStore = False
      if isStore:
        h_all_system[info.channel+"__"+info.process+"__"+info.systematic+"__"+info.shift] = file.Get(key).Clone()
        output.cd()
        h_all_system[info.channel+"__"+info.process+"__"+info.systematic+"__"+info.shift].Write()
       
#addq2File(0.30,  'ele_theta_bdt0p5_chi30_rebinned.root','M_{t#bar{t}} [GeV/c^{2}]',['ttbar','wjets_l','diboson','qcd','wjets_b','wjets_c'])
addq2File(0.30,  'ele_theta_bdt0p5_chi30_rebinned.root','M_{t#bar{t}} [GeV/c^{2}]',['ttbar','wjets_l'])
addq2File(0.30,  'mu_theta_bdt0p5_chi30_rebinned.root','M_{t#bar{t}} [GeV/c^{2}]',['ttbar','wjets_l'])
