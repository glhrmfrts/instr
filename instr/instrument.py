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
    self.segcount = 0
    self.nframes = 0
    self.fx = [(0, lambda sig, samp, x: samp)]

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
    self.segcount = len(self.segments)
    return self

  def loop(self, times, segments):
    self.segments += segments * times
    self.segcount = len(self.segments)
    return self

  def bind(self, *fx):
    for f in fx:
      self.fx.append((self.segcount, f))
    return self

  def applyfx(self, sig, samp, x, seg):
    if len(self.fx) > 1:
      samp = reduce((lambda s, fx: fx[1](sig, s, x) if seg >= fx[0] else s), [samp] + self.fx)
    return samp

  def compute(self):
    for channel in self.channels:

      # was this channel already computed?
      computed = len(channel) > 0
      if not computed:
        for iseg, seg in enumerate(self.segments):
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

          # Pre-create all samples
          sig.samples = [0] * int(math.ceil(sig.length))
          length = int(sig.length)
          for i in range(length * 2):
            if i >= sig.length:
              samp = sig.samples[i - length]
              sig.samples[i - length] = self.applyfx(sig, samp, i, iseg)
            else:
              sig.samples[i] = self.samplegenfun(sig, i)
              self.nframes += 1

          channel.append(sig)
        else:
          for i, sig in enumerate(channel):
            for x in range(int(sig.length)):
              sig.samples[x] = self.applyfx(sig, sig.samples[x], x, i)

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