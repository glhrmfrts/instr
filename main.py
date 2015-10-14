from instr.instruments import *
from instr.effects import *

b = Osc().bind(fadein(0.5))
b.seg([(440, 2)]).bind(fadeout(0.5)).seg([(660, 2)]).save('tests/instr.wav')