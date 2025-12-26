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
            custom_tooltip = {{
                text = htc_colonial_charter_why
                scope:actor = {{
                    or = {{
                        # player
                        and = {{
                            is_ai = no
                            root = {{
                                any_location_in_province_definition = {{
                                    adjacent_to_owned_by = scope:actor
                                }}
                            }}
                        }}
                        # CNs
                        and = {{
                            is_subject_type = colonial_nation
                            country_tax_base > 50
                            root.region = scope:actor.capital.region
                        }}
                        # mesoamericans
                        and = {{
                            religion.group = religion_group:tonal_group
                            root = {{
                                any_location_in_province_definition = {{
                                    adjacent_to_owned_by = scope:actor
                                }}
                            }}
                        }}
                        # incans
                        and = {{
                            religion = religion:inti
                            root.region = region:andes_region
                        }}
                        # manchuria
                        and = {{
                            has_or_had_tag = MCH
                            root.region = region:manchuria_region
                        }}
                        # japan
                        and = {{
                            or = {{
                                has_or_had_tag = YMT
                                has_or_had_tag = JAP
                            }}
                            root.continent = continent:asia
                        }}
                        # russia early
                        and = {{
                            culture = {{ has_culture_group = culture_group:russian_group }}
                            or = {{
                                root.sub_continent = sub_continent:eastern_europe
                            }}
                        }}
                        # russia late
                        and = {{
                            current_year > 1500
                            culture = {{ has_culture_group = culture_group:russian_group }}
                            or = {{
                                root.sub_continent = sub_continent:north_asia
                                root.sub_continent = sub_continent:central_asia
                            }}
                        }}
                        # natives
                        and = {{
                            not = {{ is_subject_type = colonial_nation }}
                            or = {{
                                # africa
                                has_or_had_tag = ETH
                                has_or_had_tag = KIT
                                and = {{
                                    has_or_had_tag = ZMW
                                    tax_base > 40
                                }}
                                and = {{
                                    has_or_had_tag = ZAN
                                    tax_base > 40
                                }}
                                 # kongo
                                and = {{
                        		    religion = religion:bantu_religion
                                    capital.region = region:kongo_region
                                }}
                            }}
                        }}
                        # scandinavia
                        and = {{
                            or = {{
                                has_or_had_tag = SWE
                                has_or_had_tag = NOR
                            }}
                            root.region = region:scandinavian_region
                        }}
                        {filters}
                    }}
                }}
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
        add = "scope:actor.colonial_charter_utility(scope:target)"
        if = {{
            limit = {{
                scope:actor = {{
                    or = {{
                        capital.continent = continent:europe
                        is_subject_type = colonial_nation
                    }}
                }}
            }}
            multiply = 10
        }}
    }}
}}
'''