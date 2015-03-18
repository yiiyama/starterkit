#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"

unsigned const NMAX = 256;

void
muonpt()
{
  // Open the input file
  TFile* source = TFile::Open("/scratch/yiiyama/starterkit/singlemuA.root");

  // Create handle to the ntuples object within the file
  TTree* events = (TTree*)source->Get("events");

  // Define branch variables
  unsigned muon_n;
  float muon_pt[NMAX];
  bool muon_isTight[NMAX];
  bool muon_isSoft[NMAX];

  // Associate variables to branches
  // Note that the second argument has to be the memory address of the variable.
  events->SetBranchAddress("muon.n", &muon_n);
  events->SetBranchAddress("muon.pt", muon_pt);
  events->SetBranchAddress("muon.isTight", muon_isTight);
  events->SetBranchAddress("muon.isSoft", muon_isSoft);

  // Open an output file to save the histograms
  TFile* outputFile = TFile::Open("muonpt.root", "recreate");

  // Define histograms
  // The second argument up to the first semicolon is the title of the histogram.
  // Between the two semicolons is the title of the X axis,
  // and the last bit is the title of the Y axis.
  TH1* tight = new TH1F("histo_muon_pt", "Tight muons;Muon p_{T} (GeV);events / GeV", 100, 0.0, 100.0);
  TH1* soft = new TH1F("histo_muon_pt_soft", "Soft muons;Muon p_{T} (GeV);events / GeV", 100, 0.0, 100.0);

  // Loop over entries
  // GetEntry function fetches the branch values of the given event to the assigned variables.
  // iEntry variable is incremented until GetEntry returns 0, which signifies the end of the tree.
  long iEntry = 0;
  while(events->GetEntry(iEntry++) > 0){

    // Loop over muons in the event
    for(unsigned iM = 0; iM != muon_n; ++iM){
      // If the muon passes the tight selection, fill the tight histogram
      if(muon_isTight[iM]){
        tight->Fill(muon_pt[iM]);
      }
      // If the muon passes the soft selection, fill the soft histogram
      if(muon_isSoft[iM]){
        soft->Fill(muon_pt[iM]);
      }
    }
  }

  // Set line color of the soft histogram
  soft->SetLineColor(kRed);

  // Create a canvas for the plots
  TCanvas* c1 = new TCanvas("c1", "c1");

  // Draw plots
  tight->Draw();
  soft->Draw("same");

  outputFile->cd();
  tight->Write();
  soft->Write();
}
