

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