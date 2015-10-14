def fadein(t):
	def fn(samp, dur, a, p, x):
		mdur = t * dur
		return samp * min(a / a, a * (x / mdur) / a)
	return fn

def fadeout(t):
	def fn(samp, dur, a, p, x):
		mdur = t * dur
		return samp * min(a / a, a * ((dur - x) / mdur) / a)
	return fn

def fades(tin, tout):
	return lambda s, d, a, p, x: fadeout(tout)(fadein(tin)(s, d, a, p, x), d, a, p, x)