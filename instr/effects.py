import math
from instr.instruments import Osc

"""
  An effect is a function of type:

  Signal -> [number]

  The signal is the current signal being processed.

  Some effects may need all samples together, not just of
  a invidual signal, so they have 'final=True' defined
  and their type is:

  [number] -> [number]

  The function must return new samples, processed
  by the effect.

  Usually effects are wrapped in an outside function
  that can have custom parameters.
"""

class Effect(object):

  def __init__(self, fn, final=False):
    self.fn = fn
    self.final = final

  def __call__(self, sig, rate=44100):
    return self.fn(sig) if not self.final else self.fn(sig, rate)


def fadein(t):
  def fn(sig):
    out = [0] * int(sig.length)
    for x in xrange(int(sig.length)):
      mdur = t * sig.framerate
      out[x] = sig.samples[x] * min(sig.vol, sig.vol * (x / mdur))
    return out
  return Effect(fn)

def fadeout(t):
  def fn(sig):
    out = [0] * int(sig.length)
    for x in range(int(sig.length)):
      mdur = t * sig.framerate
      out[x] = sig.samples[x] * min(sig.vol, sig.vol * ((sig.length - x) / mdur))
    return out
  return Effect(fn)

def fades(tin, tout):
  def fn(sig):
    sig.samples = fadein(tin)(sig)
    out = fadeout(tout)(sig)
    return out
  return Effect(fn)

def echo(dist, decay):
  def fn(samples, rate):
    out = samples.copy()
    d = dist * rate
    length = len(samples)
    for x in range(length):
      if x + d < length:
        # mod = int((modwave[x] / 2 + 0.5))
        out[int(x + d)] += (out[x] - out[x] * decay)# + mod
    return out

  # The echo needs all signals together
  return Effect(fn, final=True)
