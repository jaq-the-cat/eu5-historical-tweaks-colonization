from dataclasses import dataclass

@dataclass(frozen=True)
class ColonizeAction:
    TEMPLATE = '''
REPLACE:create_colonial_charter = {{
    type = owncountry
    
    potential = {{
        scope:actor = {{
            num_provinces > 0
            is_rebel_country = no
            NOT = {{ country_type = building }}
            modifier:can_colonize = yes
            OR = {{
                is_ai = no 
                ai_country_should_colonize = yes
            }}
        }}
    }}

    allow = {{
        scope:actor = {{
            total_population >= 5
        }}
    }}

    ai_tick = monthly
    ai_tick_frequency = 6
    automation_tick = monthly
    automation_tick_frequency = 1

    player_automated_category = colonies
    
    price = price:create_colonial_charter
    
    select_trigger = {{
        top_widget = colony_item_card_at_province_select
        looking_for_a = province_definition
        source = actor
        source_flags = possible_colonial_charters
        target_flag = target
        cache_targets = yes #these are the same no matter where we're coming from
        name = "create_colonial_charter_select_province_definition"
        none_available_msg_key = "create_colonial_charter_no_provinces"
        column = {{
            data = colonial_charter
        }}
        # no trigger, possible_colonial_charters does this for us in code
        # scope:actor = colonizer, root = province_definition
        enabled = {{
            scope:actor = {{
                is_valid_colonial_charter = prev
                custom_tooltip = {{
                    text = settle_the_frontier_ct
                    not = {{
                        any_cabinet = {{
                            has_cabinet_action = yes
                            cabinet_action = cabinet_action:settle_the_frontier
                            interaction_target:target = root
                        }}
                    }}
                }}
            }}
            
            or = {{
                custom_tooltip = {{
                    text = htc_player_no_restrictions_why
                    and = {{
                        scope:actor = {{ is_ai = no }}
                        has_game_rule = htc_player_no_restrictions
                    }}
                }}
                ### country restrictions
                trigger_if = {{
                    limit = {{
                        scope:actor = {{
                            is_subject_type = colonial_nation
                            or = {{
                                is_ai = no
                                country_tax_base > 50
                            }}
                        }}
                    }}
                    or = {{
                        region = scope:actor.capital.region
                        any_location_in_province_definition = {{
                            adjacent_to_owned_by = scope:actor
                        }}
                    }}
                }}
                trigger_else_if = {{
                    limit = {{
                        scope:actor.religion.group = religion_group:tonal_group
                    }}
                    root = {{
                        any_location_in_province_definition = {{
                            adjacent_to_owned_by = scope:actor
                        }}
                    }}
                }}
                trigger_else_if = {{
                    limit = {{ scope:actor.religion = religion:inti }}
                    region = region:andes_region
                }}
                trigger_else_if = {{
                    limit = {{
                        scope:actor = {{
                            or = {{
                                has_or_had_tag = ETH
                                has_or_had_tag = KIT
                                religion = religion:bantu_religion
                            }}
                        }}
                    }}
                    region = scope:actor.capital.region
                }}
                trigger_else_if = {{
                    limit = {{
                        scope:actor = {{
                            has_or_had_tag = ZAN
                            has_or_had_tag = ZMW
                        }}
                    }}
                    trigger_if = {{
                        limit = {{ scope:actor = {{ is_ai = yes }} }}
                        current_year > 1550
                    }}
                    sub_continent = capital.sub_continent
                }}
                ### regional restrictions
                trigger_if = {{
                    limit = {{
                        region = region:scandinavian_region
                    }}
                    scope:actor = {{
                        or = {{
                            current_year > 1500
                            has_or_had_tag = SWE
                            has_or_had_tag = NOR
                            has_or_had_tag = FIN
                            has_or_had_tag = DEN
                        }}
                    }}
                }}
                trigger_else_if = {{
                    limit = {{
                        region = region:manchuria_region
                    }}
                    scope:actor = {{
                        or = {{
                            current_year > 1600
                            has_or_had_tag = MCH
                        }}
                    }}
                }}
                trigger_else_if = {{
                    limit = {{
                        region = region:japan_region
                    }}
                    scope:actor = {{
                        or = {{
                            current_year > 1600
                            has_or_had_tag = YMT
                            has_or_had_tag = JAP
                        }}
                    }}
                }}
                ### autogenerated restrictions
                {filters}
            }}
        }}
    }}

    effect = {{
        scope:actor = {{
            if = {{
                limit = {{
                    exists = scope:target
                }}
                create_colonial_charter = {{
                    target = scope:target
                }}
            }}
        }}
    }}

    ai_will_do = {{
        if = {{
            limit = {{
                scope:actor = {{
				    monthly_balance > 1
                }}
            }}
            add = "scope:actor.colonial_charter_utility(scope:target)"
        }}
        else = {{
            add = -1000
        }}
    }}
}}
'''