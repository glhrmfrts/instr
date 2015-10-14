from instr.instruments import *
from instr.effects import *

Saw().bind(echo(0.4, 0.5)).loop(4, [(220, 0.1), (1, 0.9), (265, 0.1), (1, 0.9)]).save('tests/instr.wav')