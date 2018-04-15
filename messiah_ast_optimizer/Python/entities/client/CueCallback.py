CUECALLBACK = {}

enableInnerEffect = False


def enableOptimize(en):
	if not hasattr(MCharacter, "AutoPlayEffect"):
		return
	if not hasattr(MCharacter, "AutoPlaySound"):
		return
	global enableInnerEffect
	enableInnerEffect = en
	MCharacter.AutoPlayEffect(en)
	MCharacter.AutoPlaySound(en)
	MCharacter.SetEffectCacheCount(128)
	if hasattr(MCharacter, 'SetEnableTachVisible'):
		MCharacter.SetEnableTachVisible(1)


enableOptimize(True)


def CueCallbackDef(cue_type):
	def arrange(func):
		coname = sys._getframe(1).f_code.co_name
		if coname not in CUECALLBACK:
			CUECALLBACK[coname] = {}
		CUECALLBACK[coname][cue_type] = func
		return func
	return arrange


class CueCallbackComponent(object):
	def signalNotifyCallback(self, targetentity, trigger, stype, signalStr):
		pass
