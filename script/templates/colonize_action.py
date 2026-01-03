from dataclasses import dataclass

@dataclass(frozen=True)
class ColonizeAction:
    TEMPLATE_TOP ='''REPLACE:create_colonial_charter = {
    type = owncountry
    
    potential = {
        scope:actor = {
            num_provinces > 0
            is_rebel_country = no
            NOT = { country_type = building }
            modifier:can_colonize = yes
            OR = {
                is_ai = no 
                ai_country_should_colonize = yes
            }
        }
    }

    allow = {
        scope:actor = {
            total_population >= 5
        }
    }

    ai_tick = monthly
    ai_tick_frequency = 6
    automation_tick = monthly
    automation_tick_frequency = 1

    player_automated_category = colonies
    
    price = price:create_colonial_charter
    
    select_trigger = {
        top_widget = colony_item_card_at_province_select
        looking_for_a = province_definition
        source = actor
        source_flags = possible_colonial_charters
        target_flag = target
        cache_targets = yes #these are the same no matter where we're coming from
        name = "create_colonial_charter_select_province_definition"
        none_available_msg_key = "create_colonial_charter_no_provinces"
        column = {
            data = colonial_charter
        }
        # no trigger, possible_colonial_charters does this for us in code
        # scope:actor = colonizer, root = province_definition
        enabled = {
            scope:actor = {
                is_valid_colonial_charter = prev
                custom_tooltip = {
                    text = settle_the_frontier_ct
                    not = {
                        any_cabinet = {
                            has_cabinet_action = yes
                            cabinet_action = cabinet_action:settle_the_frontier
                            interaction_target:target = root
                        }
                    }
                }
            }
            ### check if player & no player restrictions is on
            trigger_if = {
                limit = {
                    scope:actor = { is_ai = no }
                    has_game_rule = htc_player_no_restrictions
                }
                always = yes
            }
            trigger_else_if = {
                limit = {
                    scope:actor = {
                        or = {
                            is_ai = no
                            # europeans
                            capital ?= { sub_continent = sub_continent:western_europe }
                            culture = { has_culture_group = culture_group:russian_group }
                            # other possible colonial powers
                            has_or_had_tag = MAL
                            has_or_had_tag = TUR
                            has_or_had_tag = OMA
                            has_or_had_tag = CHI
                            has_or_had_tag = INC
                            culture = { has_culture_group = culture_group:japanese_group }
                            # natives
                            religion.group = religion_group:tonal_group
                            culture.language = language:kongo_language
                            has_or_had_tag = ZAN
                            has_or_had_tag = ZMW
                        }
                    }
                }
                or = {
                    # game rule tooltip, not check
                    custom_tooltip = {
                        text = htc_player_no_restrictions_why
                        and = {
                            scope:actor = { is_ai = no }
                            has_game_rule = htc_player_no_restrictions
                        }
                    }
                    ### natives
                    trigger_if = {
                        limit = { scope:actor.religion.group = religion_group:tonal_group }
                        or = {
                            region = region:aridoamerica_region
                            region = region:mesoamerica_region
                            region = region:central_america_region
                        }
                        any_location_in_province_definition = {
                            adjacent_to_owned_by = scope:actor
                        }
                    }
                    trigger_else_if = {
                        limit = { scope:actor.religion = religion:inti }
                        region = region:andes_region
                    }
                    trigger_else_if = {
                        limit = { scope:actor.culture.language = language:kongo_language }
                        region = region:kongo_region
                    }
                    trigger_else_if = {
                        limit = {
                            scope:actor = {
                                has_or_had_tag = ZAN
                                has_or_had_tag = ZMW
                            }
                        }
                        current_year >= 1600
                        region = scope:actor.capital.region
                    }
                    ### region restrictions
                    trigger_if = {
                        limit = { region = region:japan_region }
                        or = {
                            current_year >= 1500
                            scope:actor.culture = { has_culture_group = culture_group:japanese_group }
                        }
                    }
                    trigger_else_if = {
                        limit = { region = region:scandinavian_region }
                        or = {
                            current_year >= 1500
                            scope:actor.culture = { has_culture_group = culture_group:scandinavian_group }
                        }
                        
                    }
                    ### siberia
                    trigger_else_if = {
                        limit = { region = region:west_siberia_region }
                        current_year >= 1560
                        or = {
                            culture = { has_culture_group = culture_group:russian_group }
                        }
                    }
                    trigger_else_if = {
                        limit = { sub_continent = sub_continent:north_asia }
                        current_year >= 1600
                        or = {
                            culture = { has_culture_group = culture_group:russian_group }
                        }
                    }
                    ### autogenerated restrictions
                    '''

    TEMPLATE_BOTTOM = '''
                }
            }
        }
    }

    effect = {
        scope:actor = {
            if = {
                limit = {
                    exists = scope:target
                }
                create_colonial_charter = {
                    target = scope:target
                }
            }
        }
    }

    ai_will_do = {
        if = {
            limit = {
                scope:actor = {
				    monthly_balance > 1
                    or = {
                        has_colonial_charters = yes
                        is_colonial_top_overlord = yes
                        scope:target = {
                            any_location_in_province_definition = {
                                adjacent_to_owned_by = scope:actor
                            }
                        }
                    }
                }
            }
            add = "scope:actor.colonial_charter_utility(scope:target)"
        }
        else = {
            add = -1000
        }
    }
}
'''