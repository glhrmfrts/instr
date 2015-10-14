import wave, struct, math
from functools import reduce

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


class Instrument(object):
  
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
    self.nframes = 0
    self.fx = [lambda sig, samp, x: samp]

  def __add__(self, other):
    res = Instrument()
    res.channels = self.computeget() + other.computeget()
    res.nframes = self.nframes + other.nframes
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
    return self

  def loop(self, times, segments):
    self.segments += segments * times
    return self

  def bind(self, *fx):
    self.fx += fx
    return self

  def applyfx(self, sig, samp, x):
    transformed = samp
    if len(self.fx) > 1:
      transformed = reduce(lambda s, f: f(sig, s, x), [samp] + self.fx)
    return transformed

  def compute(self):
    for channel in self.channels:

      # was this channel already computed?
      computed = len(channel) > 0
      if not computed:
        for seg in self.segments:

          freq, dur, vol = 0, 0, 1
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
          sig = Signal(freq, self.framerate, dur, self.amp, vol)

          for i in range(sig.length):
            pure = self.samplegenfun(sig, i)
            sig.samples.append(self.applyfx(sig, pure, i))

          self.nframes += sig.length
          channel.append(sig)
        else:
          for sig in channel:
            for x in range(sig.length):
              sig.samples[x] = self.applyfx(sig, sig.samples[x], x)

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

    for signals in zip(*self.channels):
      samples = []
      samples += map(lambda s: s.samples, list(signals))
      
      for pair in zip(*samples):
        for s in list(pair):
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