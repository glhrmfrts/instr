"""
	An effect is a function of type:

	Signal -> number -> number -> number

	The signal is the current signal being processed,
	the second parameter is the current sample of that signal,
	the third is the index of the samples (aka the 'tick' or the 'x' of the equation)

	The function must return a new number, which is
	the sample processed by the fx

	Usually effects are wrapped in an outside function
	that can have custom parameters.
"""

def fadein(t):
	def fn(sig, samp, x):
		mdur = t * sig.length
		return samp * min(sig.vol, (x / mdur))
	return fn

def fadeout(t):
	def fn(sig, samp, x):
		mdur = t * sig.length
		return samp * min(sig.vol, ((dur - x) / mdur))
	return fn

def fades(tin, tout):
	return lambda sig, samp, x: fadeout(tout)(sig, fadein(tin)(sig, samp, x), x)