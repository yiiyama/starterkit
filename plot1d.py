#! /usr/bin/env python

#----------------------------------------------------------------------
# Sample usage
# ./plot1d.py
#----------------------------------------------------------------------

import sys
import os
import ROOT
from optparse import OptionParser

# - M A I N ----------------------------------------------------------------------------------------

# Parse the input (options for later use)
parser = OptionParser()
parser.add_option("-f", "--file", dest="inputFileName",
                  default='/scratch5/dimatteo/cms/hist/boostedv-v13/merged-dev/boostedv-v13_s12-zll-ptz100-v7c_noskim_flatntuple.root',
                  help="input root file [default: %default]")
parser.add_option("-t", "--treename", dest="inputTreeName",
                  default='DMSTree',
                  help="root tree name [default: %default]")
(options, args) = parser.parse_args()

# Check for initialization macro
rootlogon = ROOT.gEnv.GetValue("Rint.Logon", "")

# Run the macro if it exists (necessary when running ROOT from python)
if rootlogon:
    ROOT.gROOT.Macro(rootlogon)

# Check and open the input file
input_file = ROOT.TFile.Open(options.inputFileName)
if input_file:
    print 'INFO - Opening input root file: ' + options.inputFileName
else:
    print 'ERROR - Cannot open input root file: ' + options.inputFileName + ' , exiting!'
    raise SystemExit

# Retrieve the input tree from input file
input_tree = input_file.FindObjectAny(options.inputTreeName)
if input_tree:
    print 'INFO - Opening root tree: ' + options.inputTreeName
else:
    print 'ERROR - Cannot open root tree: ' + options.inputTreeName + ' , exiting!'
    raise SystemExit

# Check the number of entries in the tree
n_entries = input_tree.GetEntriesFast()
print 'INFO - Input tree entries: ' + str(n_entries)

# Prepare the histogram for plotting the variable number of electrons
# -> 1-D Histograms are all constructed with the follwing input
# -> "name","title",number_of_bins,min,max
h_nele = ROOT.TH1F('h_nele', 'Number of electrons', 4, 0, 4)

# Prepare the name of the variable that you want to look at
variable_name = 'nele'

# Fill the histogram in one simple command!
input_tree.Draw(variable_name + ' >> ' + h_nele.GetName(),'','goff')

# Prepare histogram axis titles
h_nele.GetXaxis().SetTitle("number of electrons")
h_nele.GetYaxis().SetTitle("entries")

# Plot the histogram on a TCanvas
c1 = ROOT.MitRootStyle.MakeCanvas('c1', 'My First plot')
ROOT.MitRootStyle.InitSubPad(c1)
h_nele.Draw()

# Now prepare the histograms for the invariant mass of the di-electron system
# -> "name","title",number_of_bins,min,max
h_mee = ROOT.TH1F('h_mee', 'Di-Electron invariant mass', 100, 0, 200)

# Prepare the name of the variable that you want to look at
# -> you can plot not obly variables, but expressions which are functions of the variables
expression = 'sqrt((ele1.E()+ele2.E())**2-(ele1.Px()+ele2.Px())**2-(ele1.Py()+ele2.Py())**2-(ele1.Pz()+ele2.Pz())**2)'

# Fill the histogram in one simple command!
input_tree.Draw(expression + ' >> ' + h_mee.GetName(),'nele > 2','goff')

# Prepare histogram axis titles
h_mee.GetXaxis().SetTitle("m_{ee} [GeV]")
h_mee.GetYaxis().SetTitle("entries")

# Plot the histogram on a TCanvas
c2 = ROOT.MitRootStyle.MakeCanvas('c2', 'My Second plot')
ROOT.MitRootStyle.InitSubPad(c2)
h_mee.Draw()

# Create a directory for images if it does not already exist
if not os.path.isdir('imgs'):
    os.mkdir('imgs')

# Now save the canvas into two nice png files
# Other allowed formats: jpg, pdf, etc. Details at https://root.cern.ch/root/html532/TPad.html#TPad:Print%1
c1.SaveAs('imgs/nele.png','png')
c2.SaveAs('imgs/mee.png','png')

## wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
rep = ''
while rep not in [ 'q', 'Q' ]:
    sys.stdout.write('enter "q" to quit: ')
    sys.stdout.flush()
    rep = sys.stdin.readline().strip()
