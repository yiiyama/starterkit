if [[ $(uname -r) =~ el6 ]]; then
    CWD=$PWD
    export SCRAM_ARCH=slc6_amd64_gcc491
    export MIT_ROOT_STYLE=STARTERKIT/MitRootStyle
    export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
    source $VO_CMS_SW_DIR/cmsset_default.sh
    cd CMSSW_BASE
    eval `scram runtime -sh`
    cd $CWD
else
    echo "Please log in to an SL6 machine."
fi
