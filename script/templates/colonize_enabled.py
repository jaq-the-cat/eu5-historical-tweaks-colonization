from dataclasses import dataclass

@dataclass(frozen=True)
class ColonizeEnabled:
    TAG_TEMPLATE = '''has_or_had_tag = {tag}
                                '''
    GEO_FILTER_TEMPLATE = '''and = {{
                                        current_year > {year}
                                        {geography_select} = {geography_type}:{geography}
                                    }}
                                    '''
    FILTER_TEMPLATE = '''# {comment}
                        and = {{
                            or = {{
                                is_ai = no
                                {tags}
                            }}
                            root = {{
                                or = {{
                                    {geo_filters}
                                }}
                            }}
                        }}
                        '''