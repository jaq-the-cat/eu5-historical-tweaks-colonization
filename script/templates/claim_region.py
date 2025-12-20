from dataclasses import dataclass
from templates import TemplateData

@dataclass(frozen=True)
class ClaimRegion(TemplateData):
	NAMESPACE = 'htc_claim_region_{name}'

	LOCALIZATION_TEMPLATE = '''
  htc_claim_region_{name}.{n}.title: ""
  htc_claim_region_{name}.{n}.desc: ""
'''[1:]

	EVENT_TEMPLATE = '''htc_claim_region_{name}.{n} = {{
		type = country_event
		title = htc_claim_region_{name}.{n}.title
		desc = htc_claim_region_{name}.{n}.desc
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
			region:{geography} = {{
				any_location_in_region = {{
					is_discovered_by = root
					within_colonial_range_of = root
				}}
				any_province_definition = {{
					filter = {{ region = region:{geography} }}
					not = {{
						any_present_country = {{
							filter = {{ has_colonial_charters = yes }}
							has_colonial_charter_in = prev
						}}
					}}
				}}
			}}
		}}
		
		immediate = {{
			region:{geography} = {{
				save_scope_as = geo
			}}
		}}
		

		option = {{
			name = htc.options.claim
			historical_option = yes
			
			every_province_definition = {{
				limit = {{
					region = region:{geography}
				}}
				root = {{
					create_colonial_charter = {{
						target = province_definition:{geography}
					}}
				}}
			}}
		}}
		option = {{
			name = htc.options.no
		}}
	}}
	'''