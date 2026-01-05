from lib.enable_generator import CharterFilterGenerator
from lib.events_generator import ColonyEventGenerator
from templates.create_colonial_charter.colonize_action import ColonizeAction
import os

def enable_charters():
    for dirpath, dirnames, filenames in os.walk('colonies/enable'):
        filters = []
        for file in filenames:
            g = CharterFilterGenerator(os.path.join(dirpath, file))
            filters.append(g.get_enabled_filter())

        with open(os.path.join('../in_game/common/generic_actions/htc_colonial_charters_generated.txt'), 'w', encoding='utf-8-sig') as file:
            file.write(
                ColonizeAction.TEMPLATE_TOP +
                ''.join(filters).rstrip() +
                ColonizeAction.TEMPLATE_BOTTOM)

def charter_events():
    for dirpath, dirnames, filenames in os.walk('colonies/events'):
        filters = []
        for file in filenames:
            g = ColonyEventGenerator(os.path.join(dirpath, file))
            g.write_all('../in_game/events/generated')

enable_charters()
charter_events()