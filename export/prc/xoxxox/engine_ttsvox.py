import json
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
from xoxxox.shared import Custom
from xoxxox.params import Config
from xoxxox.params_vox import AppVox

#---------------------------------------------------------------------------

class TtsPrc():

  def __init__(self, config="xoxxox/config_ttsvox_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.keyspk = ""
    self.mdlvvm = ""
    pthrun = "onnxruntime/lib/" + Onnxruntime.LIB_VERSIONED_FILENAME
    pthdic = "dict/open_jtalk_dic_utf_8-1.11"
    self.nmodel = Synthesizer(Onnxruntime.load_once(filename=pthrun), OpenJtalk(pthdic))
    with open(Config.dircnf + "/" + AppVox.cnfspk, "r") as f:
      self.dicspk = json.load(f)

  def status(self, config="xoxxox/config_ttsvox_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    if self.keyspk != diccnf["keyspk"]:
      self.keyspk = diccnf["keyspk"]
      if self.mdlvvm != self.dicspk[self.keyspk]["vvm"]:
        self.mdlvvm = self.dicspk[self.keyspk]["vvm"]
        try:
          with VoiceModelFile.open("models/vvms/" + self.mdlvvm) as m:
            self.nmodel.load_voice_model(m)
        except Exception as e:
          print("err[" + str(e) + "]", flush=True) # DBG

  def infere(self, txtreq):
    datwav = self.nmodel.tts(txtreq, int(self.keyspk))
    return datwav
