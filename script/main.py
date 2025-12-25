from lib.enable_generator import CharterFilterGenerator
from templates.colonize_action import ColonizeAction
import os

for dirpath, dirnames, filenames in os.walk('colonies/enable'):
    filters = []
    for file in filenames:
        g = CharterFilterGenerator(os.path.join(dirpath, file))
        filters.append(g.get_enabled_filter())

    with open(os.path.join('../in_game/common/generic_actions/htc_colonial_charters_generated.txt'), 'w', encoding='utf-8-sig') as file:
        action = ColonizeAction.TEMPLATE.format(filters=''.join(filters).rstrip())
        file.write(action)
