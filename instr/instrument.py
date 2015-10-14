import wave, struct, math
from functools import reduce

class Instrument(object):
	
	def __init__(self):
		self.a = 1
		self.volume = 5000
		self.framerate = 44100
		self.sampwidth = 2
		self.freq = 440
		self.dur = 1
		self.samples = []
		self.channels = [self.samples]
		self.signalgenfun = None
		self.segments = []
		self.fx = [lambda s, d, a, p, x: s]

	def __add__(self, other):
		res = Instrument()
		res.channels = self.computeget() + other.computeget()
		print(len(res.channels))
		return res

	def seta(self, a):
		self.a = a
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

	def applyfx(self, samp, d, a, p, x):
		transformed = samp
		if len(self.fx) > 1:
			transformed = reduce(lambda s, f: f(s, d, a, p, x), [samp] + self.fx)
		return self.a * transformed

	def compute(self):
		for channel in self.channels:

			# was this channel already computed?
			computed = len(channel) > 0

			for seg in self.segments:
				freq, dur, amp = 0, 0, 1
				if isinstance(seg, tuple):
					freq = seg[0]
					try:
						dur = seg[1]
						amp = seg[2]
					except IndexError:
						pass
				else:
					freq = self.freq
					dur = self.dur
					amp = seg
				period = self.framerate / freq
				sampdur = int(self.framerate * dur)
				for i in range(sampdur):
					transform = lambda p: self.applyfx(p, sampdur, amp * self.volume, period, i)
					if not computed:

						# samples were not processed yet
						pure = self.signalgenfun(int(self.framerate * dur), amp * self.volume, period, i)
						channel.append(transform(pure))
					else:

						# samples already computed, only apply effects
						pure = channel[i]
						channel[i] = transform(pure)

	def computeget(self):
		self.compute()
		return self.channels

	def save(self, filename):
		self.compute()

		fh = wave.open(filename, 'w')
		fh.setnchannels(len(self.channels))
		fh.setsampwidth(self.sampwidth)
		fh.setframerate(self.framerate)
		samples = list(zip(*self.channels))
		fh.setnframes(len(samples))

		for i in range(len(samples)):
			samp = samples[i]
			for s in list(samp):
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