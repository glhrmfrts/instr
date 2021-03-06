import operator

class Signal(object):

  def __init__(self, f, fr, dur, a, v):
    self.frequency = f
    self.framerate = fr
    self.period = fr / f

    # Duration of the signal in seconds
    self.dur = dur

    # Number of samples
    self.length = fr * dur

    # Amplitude is a big number which is what actually
    # the signal is multiplied by
    self.amp = a

    # Volume is like a 'knob' controlling the amplitude,
    # it's a number between 0 and 1
    self.vol = v
    self.a = a * v

    self.samples = []

  def arith(self, op, other):
    if type(other) in ['int', 'float']:
      for x in range(len(self)):
        self[x] = op(self, other)

  def __add__(self, other):
    self.arith(operator.add, other)

  def __sub__(self, other):
    self.arith(operator.sub, other)

  def __mul__(self, other):
    self.arith(operator.mul, other)

  def __div__(self, other):
    self.arith(operator.div, other)

  def __len__(self):
    return int(self.length)

  def __getitem__(self, x):
    return self.samples[x]

  def __setitem__(self, x, v):
    self.samples[x] = v