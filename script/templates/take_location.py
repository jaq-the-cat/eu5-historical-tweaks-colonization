from dataclasses import dataclass
from templates import TemplateData

@dataclass(frozen=True)
class TakeLocation(TemplateData):
	NAMESPACE = 'htc_take_location_{name}'

	LOCALIZATION_TEMPLATE = '''
  htc_take_location_{name}.{n}.title: ""
  htc_take_location_{name}.{n}.desc: ""
'''[1:]

	EVENT_TEMPLATE = '''htc_take_location_{name}.{n} = {{
		type = country_event
		title = htc_take_location_{name}.{n}.title
		desc = htc_take_location_{name}.{n}.desc
		fire_only_once = yes
		
		dynamic_historical_event = {{
{tags}
			from = {from_year}.1.1
			to = {to_year}.1.1
			monthly_chance = 10
		}}

		illustration_tags = {{
			10 = happy
			10 = exterior
		}}

		trigger = {{
			location:{geography} = {{
				has_owner = no
				is_ownable = yes
				within_colonial_range_of = root
				is_discovered_by = root
			}}
		}}		

		immediate = {{
			location:{geography} = {{
				save_scope_as = geo
			}}
		}}
		

		option = {{
			name = htc.options.take
			historical_option = yes
			
			location:{geography} = {{
				change_location_owner = root
			}}
		}}
		option = {{
			name = htc.options.no
		}}
	}}
	'''