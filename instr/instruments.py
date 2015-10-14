import math
from instr.instrument import Instrument

class Osc(Instrument):

	def __init__(self):
		Instrument.__init__(self)
		self.signalgenfun = self.osc

	def osc(self, d, a, p, t):
		return a * math.sin(2 * math.pi * (t / p))


class Sqr(Instrument):

	def __init__(self):
		Instrument.__init__(self)
		self.signalgenfun = self.sqr

	def sqr(self, d, a, p, t):
		return a if (int(t / p) % 2) == 0 else -a


class Saw(Instrument):

	def __init__(self):
		Instrument.__init__(self)
		self.signalgenfun = self.saw

	def saw(self, d, a, p, t):
		return a * ((t % p) / p * 2 - 1)


class Tri(Instrument):

	def __init__(self):
		Instrument.__init__(self)
		self.signalgenfun = self.tri

	def tri(self, d, a, p ,t):
		return -a + abs((t % p) - a)