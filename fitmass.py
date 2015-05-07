from ROOT import *

workspace = RooWorkspace('workspace')

mass = workspace.factory('mass[0,1000]')
background = workspace.factory('Exponential::background(mass, c[-0.2,-10.,0.])')
signal = workspace.factory('BreitWigner::signal(mass, m0[3.69,3.3,4.])')
model = workspace.factory('SUM::model(nsig[200,0.,10000.] * signal, nbkg[1000.,0.,10000.] * background)')

source = TFile.Open('dimuonMass.root')
inputTree = source.Get('massTree')
dataset = RooDataSet('dataset', 'invariant mass', inputTree, RooArgSet(mass))

model.fitTo(dataset)

frame = mass.frame()
model.plotOn(frame, RooFit.LineStyle(kSolid), RooFit.LineWidth(2), RooFit.LineColor(kBlue))
model.plotOn(frame, RooFit.Components(background), RooFit.LineStyle(kDashed), RooFit.LineWidth(2), RooFit.LineColor(kBlue))

canvas = TCanvas('c1', 'c1', 600, 600)

frame.Draw()

canvas.Print('fitmass.pdf')
