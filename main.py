from instr.instruments import *
from instr.effects import *

sqrs = Sqr().seg([(330, 2)])
saws = Saw().seg([(440, 2)])
b = sqrs + saws
b.bind(fadein(0.5)).save('instr.wav')