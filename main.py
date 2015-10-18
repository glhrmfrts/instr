from instr.instruments import *
from instr.effects import *

s = Sqr().bind(tremolo()).seg([(244, 1), (289, 1), (365, 1)]).save('tests/instr.wav')