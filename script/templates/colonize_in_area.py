from dataclasses import dataclass
from templates import TemplateData

@dataclass(frozen=True)
class ColonizeInArea(TemplateData):
	NAMESPACE = 'htc_colonize_in_area_{name}'

	LOCALIZATION_TEMPLATE = '''
  htc_colonize_in_area_{name}.{n}.title: ""
  htc_colonize_in_area_{name}.{n}.desc: ""
'''[1:]

	EVENT_TEMPLATE = '''htc_colonize_in_area_{name}.{n} = {{
		type = country_event
		title = htc_colonize_in_area_{name}.{n}.title
		desc = htc_colonize_in_area_{name}.{n}.desc
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
			area:{geography} = {{
				any_province_definition_in_area = {{
					not = {{ has_colonial_charter = root }}
					not = {{ any_present_country = {{ has_colonial_charter_in = prev }} }}
					any_location_in_province_definition = {{
						has_owner = no
						is_ownable = yes
						is_discovered_by = root
						within_colonial_range_of = root
					}}
					is_valid_colonial_charter = yes
				}}
			}}
		}}
		
		immediate = {{
			area:{geography} = {{
				random_province_definition_in_area = {{
					limit = {{
						not = {{ has_colonial_charter = root }}
						not = {{ any_present_country = {{ has_colonial_charter_in = prev }} }}
						any_location_in_province_definition = {{
							has_owner = no
							is_ownable = yes
							is_discovered_by = root
							within_colonial_range_of = root
						}}
						is_valid_colonial_charter = yes
					}}
					save_scope_as = geo
				}}
			}}
		}}

		option = {{
			name = htc.options.take
			historical_option = yes

			create_colonial_charter = {{
				target = scope:geo
			}}
		}}
		option = {{
			name = htc.options.no
		}}
	}}
	'''