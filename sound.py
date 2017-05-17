import winsound

def playBip(go):
	if (go):
		winsound.PlaySound('bip.wav', winsound.SND_ASYNC)