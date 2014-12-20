###############################################################################
# File for running Brunel, most basic config checking VELO tracks
#
# Syntax is:
#   gaudirun.py Brunel-basic-velopix.py
##############################################################################

from Configurables import GpuService
GpuService().SocketPath = "/tmp/GpuManager"

from Brunel.Configuration import *
from Configurables import PrChecker, TrackEffChecker, PrPixelTracking
from Configurables import PrLHCbID2MCParticle, PrTrackAssociator
from Configurables import PrChecker
from Configurables import ProcessPhase, GaudiSequencer, NTupleSvc, OutputStream

from GaudiKernel.ProcessJobOptions import importOptions
importOptions("$APPCONFIGOPTS/Brunel/MC-WithTruth.py")
importOptions("$APPCONFIGOPTS/Brunel/Upgrade-RichPmt.py")
importOptions("$APPCONFIGOPTS/Brunel/patchUpgrade1.py")
importOptions("$APPCONFIGOPTS/Brunel/xdst.py")

from Configurables import Brunel

LHCbApp().DDDBtag   = "dddb-20140606"
LHCbApp().CondDBtag = "sim-20140204-vc-md100"
Brunel().DataType  = "2012"

Brunel().WithMC    = True
Brunel().InputType = "DIGI"
Brunel().Detectors = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Magnet', 'Tr' ]
# Brunel().RecoSequence = [ "HLT" ]
# Brunel().MCLinksSequence = [ "Unpack", "Tr" ]
# Brunel().MCCheckSequence = [ "Pat" ]
Brunel().OutputType = "NONE"
RecMoniConf().MoniSequence = [ ]

# Database
from Configurables import CondDB, LHCbApp
LHCbApp().EvtMax = 100
LHCbApp().Simulation = True
LHCbApp().DDDBtag = "dddb-20131025"
LHCbApp().CondDBtag = "sim-20130830-vc-md100"
CondDB().AllLocalTagsByDataType=["VP_UVP+RICH_2019+UT"]
CondDB().Upgrade = True

from Configurables import CondDB, CondDBAccessSvc
privatedbPath = "myDDDB-LHCb-Upgrade-VP-Jun2014.nom"
myAccessSvc = CondDBAccessSvc("mySuperHyperAccessSvc", ConnectionString = "sqlite_file:"+privatedbPath+".db/DDDB", CacheHighLevel = 2000)
CondDB().addLayer(accessSvc = myAccessSvc)

# Load MC data from local files
from os import listdir
containing_folder = "/home/dcampora/projects/gaudi/xdigi_thomas/"
inputFiles = [containing_folder + a for a in listdir(containing_folder) if ".digi" in a]
EventSelector().Input = inputFiles

# PrPixel options
PrPixelTracking().TimingMeasurement = True
PrPixelTracking().OutputLevel = DEBUG

def add_members():
    GaudiSequencer("RecoCALOSeq").Members = []
    GaudiSequencer("RecoMUONSeq").Members = []
    GaudiSequencer("RecoPROTOSeq").Members = []
    GaudiSequencer("RecoRICHSeq").Members = []
    #GaudiSequencer("RecoVertexSeq").Members = []
    #GaudiSequencer("TrForwardSeq").Members = []
    #GaudiSequencer("TrSeedingSeq").Members = []
    #GaudiSequencer("TrUpSeq").Members = []
    #GaudiSequencer("TrDownSeq").Members = []
    #GaudiSequencer("TrMatchSeq").Members = []
    #GaudiSequencer("TrBestSeq").Members = []
    #GaudiSequencer("TrFitSeq").Members = []
    #
    # GaudiSequencer("MCLinksUnpackSeq").Members = []
    GaudiSequencer("CaloBanksHandler").Members = []
    # GaudiSequencer("MCLinksTrSeq").Members = []
    GaudiSequencer("CheckPatSeq").Members = []
    #
    # GaudiSequencer("MCLinksCaloSeq").Members = []
    GaudiSequencer("TrUpSeq").Members = []
    GaudiSequencer("TrMatchSeq").Members = []
    GaudiSequencer("TrDownSeq").Members = []
    GaudiSequencer("RecoVertexSeq").Members = []
    GaudiSequencer("TrForwardSeq").Members = []
    GaudiSequencer("TrSeedingSeq").Members = []
    GaudiSequencer("TrBestSeq").Members = []
    GaudiSequencer("TrFitSeq").Members = []
    GaudiSequencer("CheckMUONSeq").Members = []
    GaudiSequencer("CheckRICHSeq").Members = []
    GaudiSequencer("OutputDSTSeq").Members = []
    GaudiSequencer("RecoSUMMARYSeq").Members = []

def track_checker():
    GaudiSequencer("MCLinksTrSeq").Members += [PrLHCbID2MCParticle(), PrTrackAssociator()]
    GaudiSequencer("CheckPatSeq").Members  = [PrChecker()]

appendPostConfigAction(add_members)
appendPostConfigAction(track_checker)

