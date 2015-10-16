import wave, struct, math, random
from functools import reduce
from instr.signal import Signal


class BaseInstrument(object):
  
  def __init__(self):
    self.vol = 1
    self.amp = 5000
    self.framerate = 44100
    self.sampwidth = 2
    self.freq = 440
    self.dur = 1
    self.channels = [[]]
    self.signalgenfun = None
    self.segments = []
    self.segcount = 0
    self.nframes = 0
    self.fx = [(0, lambda sig: sig.samples)]
    self.final_fx = []

  def __add__(self, other):
    res = BaseInstrument()
    res.channels = self.computeget() + other.computeget()
    res.nframes = self.nframes + other.nframes
    res.fx += self.fx + other.fx
    res.final_fx += self.final_fx + other.final_fx
    return res

  def setvol(self, a):
    self.vol = vol
    return self

  def setfreq(self, freq):
    self.freq = freq
    return self

  def setdur(self, dur):
    self.dur = dur
    return self

  def seg(self, segments):
    self.segments += segments
    self.segcount = len(self.segments)
    return self

  def loop(self, times, segments=None):
    if not segments is None:
      self.segments += segments * times
    else:
      self.segments *= times
    self.segcount = len(self.segments)
    return self

  def bind(self, *fx):
    for f in fx:
      if f.final:
        self.final_fx.append(f)
      else:
        self.fx.append((self.segcount, f))
    return self

  def single(self, frequency, dur=1, vol=1):
    """ Add a single note to the segments """
    self.segments.append( (frequency, dur, vol) )
    return self

  def sig(self, frequency, dur=1, vol=1, iseg=0):
    """ Generates a signal """
    sig = Signal(frequency, self.framerate, dur, self.amp, vol)

    sig.samples = [0] * int(math.ceil(sig.length))
    length = int(sig.length)

    for i in range(length):
      sig.samples[i] = self.samplegenfun(sig, i)
      self.nframes += 1

    self.applyfx(sig, iseg)
    return sig

  def applyfx(self, sig, seg):
    if len(self.fx) > 1:
      sig.samples = reduce((lambda s, f: f[1](sig) if seg >= f[0] else sig.samples), [sig.samples] + self.fx)

  def compute(self):
    for channel in self.channels:

      # was this channel already computed?
      computed = len(channel) > 0
      if not computed:
        for iseg, seg in enumerate(self.segments):
          freq, dur, vol = 0, 1, 1
          if isinstance(seg, tuple):
            freq = seg[0]
            try:
              dur = seg[1]
              vol = seg[2]
            except IndexError:
              pass
          else:
            freq = self.freq
            dur = self.dur
            vol = seg

          period = self.framerate / freq

          # Each segment is a new signal
          sig = self.sig(freq, dur, vol, iseg)
          channel.append(sig)

        else:
          for i, sig in enumerate(channel):
            self.applyfx(sig, i)

  def computeget(self):
    self.compute()
    return self.channels

  def save(self, filename):
    self.compute()

    fh = wave.open(filename, 'w')
    fh.setnchannels(len(self.channels))
    fh.setsampwidth(self.sampwidth)
    fh.setframerate(self.framerate)
    fh.setnframes(self.nframes)

    final = []

    for signals in zip(*self.channels):
      samples = []
      samples += map(lambda s: s.samples, list(signals))

      for pair in zip(*samples):
        final += list(pair)

    if len(self.final_fx) > 0:
      final = reduce((lambda s, fx: fx(s, self.framerate)), [final] + self.final_fx)

    for s in final:
      fh.writeframesraw(struct.pack('h', int(s)))
    
    fh.close()
    return self

  def play(self):
    try:
      import pygame
      self.save('temp.wav')
      pygame.mixer.init()
      sound = pygame.mixer.Sound('temp.wav')
      sound.play()
    except ImportError:
      print("To play a sound pygame is required")


class Osc(BaseInstrument):

  def __init__(self):
    BaseInstrument.__init__(self)
    self.samplegenfun = self.osc

  def osc(self, sig, x):
    return sig.a * math.sin(2 * math.pi * (x / sig.period))


class Sqr(BaseInstrument):

  def __init__(self):
    BaseInstrument.__init__(self)
    self.samplegenfun = self.sqr

  def sqr(self, sig, x):
    return sig.a if (int(x / sig.period) % 2) == 0 else -sig.a


class Saw(BaseInstrument):

  def __init__(self):
    BaseInstrument.__init__(self)
    self.samplegenfun = self.saw

  def saw(self, sig, x):
    return sig.a * ((x % sig.period) / sig.period * 2 - 1)


class Tri(BaseInstrument):

  def __init__(self):
    BaseInstrument.__init__(self)
    self.samplegenfun = self.tri

  def tri(self, sig, x):
    return -sig.a + abs((x % sig.period) - sig.a)


class White(BaseInstrument):
  def __init__(self):
    BaseInstrument.__init__(self)
    self.samplegenfun = self.white

  def white(self, sig, x):
    return sig.a * random.randint(-1, 1)