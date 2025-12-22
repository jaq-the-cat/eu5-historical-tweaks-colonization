from lib.parser import ColonyEventGenerator
import os

for dirpath, dirnames, filenames in os.walk('colonies'):
    for file in filenames:
        g = ColonyEventGenerator(os.path.join(dirpath, file))
        g.write_all('../in_game/events/generated')
