#!/bin/bash

if ! [[ $(uname -r) =~ el6 ]]; then
    echo "Please log in to an SL6 machine."
    exit 1
fi

STARTERKIT=$(cd `dirname $0`; pwd)
cd $STARTERKIT

echo "--------------------------------------"
echo "+ Installing CMSSW (needed for ROOT) +"
echo "--------------------------------------"

export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

scram p CMSSW CMSSW_7_3_2
if [ $? -ne 0 ]; then
    echo "Failed to set up CMSSW. Exiting"
    exit 1
fi

export CMSSW_BASE=$PWD/CMSSW_7_3_2
cd $CMSSW_BASE
eval `scram runtime -sh`

cd $STARTERKIT

echo "--------------------------------------"
echo "+ Installing MIT ROOT styles package +"
echo "--------------------------------------"

git clone https://github.com/cpausmit/MitRootStyle.git
if [ $? -ne 0 ]; then
    echo "Failed to fetch MIT ROOT styles. Exiting"
    exit 1
fi
cd MitRootStyle

# TEMPORARY
sed -i 's/root/root -n/' install.sh
# TEMPORARY

./install.sh

cd $STARTERKIT

echo "-------------------------------------"
echo "+ Setting up initialization scripts +"
echo "-------------------------------------"

cd $STARTERKIT
if [ -e $HOME/.rootrc ]; then
    cp $HOME/.rootrc $STARTERKIT/.rootrc.original
    echo "--------------------------------------------------------------"
    echo "Original rootrc file backed up at $STARTERKIT/.rootrc.original"
    echo "--------------------------------------------------------------"
fi
cp $STARTERKIT/.rootrc $HOME/

sed -i "s|STARTERKIT|$STARTERKIT|" $STARTERKIT/init.sh
sed -i "s|CMSSW_BASE|$CMSSW_BASE|" $STARTERKIT/init.sh

echo "-------------------------------------------------------------------------"
echo "Issue the following command to set the environments each time logging in:"
echo " $ source $STARTERKIT/init.sh"
echo "-------------------------------------------------------------------------"
