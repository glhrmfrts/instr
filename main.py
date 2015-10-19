from instr.instruments import *
from instr.effects import *

s = Sqr().bind(tremolo(), echo(0.4, 0.8)).loop(2, [(244, 1), (289, 1), (365, 2)]).loop(4, [(244, 0.1), (289, 0.1), (365, 0.1), (1, 0.1), (237, 0.1), (1, 0.1)]).save('tests/instr.wav')
