from lib.parser import ColonyEventGenerator
import os

for dirpath, dirnames, filenames in os.walk('colonies'):
    for file in filenames:
        g = ColonyEventGenerator(os.path.join(dirpath, file))
        g.write_all('output/', 'output/localization/localization.yml')
