import math

"""
  An effect is a function of type:

  Signal -> number -> number -> number

  The signal is the current signal being processed,
  the second parameter is the current sample of that signal,
  the third is the index of the sample (aka the 'tick' or the 'x' of the equation)

  The function must return a new number, which is
  the sample processed by the fx

  Usually effects are wrapped in an outside function
  that can have custom parameters.
"""

def fadein(t):
  def fn(sig, samp, x):
    mdur = t * sig.framerate
    return samp * min(sig.vol, sig.vol * (x / mdur))
  return fn

def fadeout(t):
  def fn(sig, samp, x):
    mdur = t * sig.framerate
    return samp * min(sig.vol, sig.vol * ((sig.length - x) / mdur))
  return fn

def fades(tin, tout):
  return lambda sig, samp, x: fadeout(tout)(sig, fadein(tin)(sig, samp, x), x)

def echo(dist, decay):
  def fn(sig, samp, x):
    d = dist * sig.framerate
    if x + d < sig.length:
      sig.samples[int(x + d)] += (samp * decay)
    return samp
  return fn
