from instr.instruments import *
from instr.effects import *

Sqr().bind(echo(0.2, 0.8)).loop(4, [(220, 0.1), (1, 0.9), (265, 0.1), (1, 0.9)]).save('tests/instr.wav')