import math, random
from instr.instrument import Instrument

class Osc(Instrument):

  def __init__(self):
    Instrument.__init__(self)
    self.samplegenfun = self.osc

  def osc(self, sig, x):
    return sig.a * math.sin(2 * math.pi * (x / sig.period))


class Sqr(Instrument):

  def __init__(self):
    Instrument.__init__(self)
    self.samplegenfun = self.sqr

  def sqr(self, sig, x):
    return sig.a if (int(x / sig.period) % 2) == 0 else -sig.a


class Saw(Instrument):

  def __init__(self):
    Instrument.__init__(self)
    self.samplegenfun = self.saw

  def saw(self, sig, x):
    return sig.a * ((x % sig.period) / sig.period * 2 - 1)


class Tri(Instrument):

  def __init__(self):
    Instrument.__init__(self)
    self.samplegenfun = self.tri

  def tri(self, sig, x):
    return -sig.a + abs((x % sig.period) - sig.a)


class White(Instrument):
  def __init__(self):
    Instrument.__init__(self)
    self.samplegenfun = self.white

  def white(self, sig, x):
    return sig.a * random.randint(-1, 1)