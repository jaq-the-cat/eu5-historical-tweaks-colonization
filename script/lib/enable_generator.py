import yaml
from os import path
from templates import *
from templates.colonize_enabled import ColonizeEnabled

def get_geography_type(s: str) -> str:
    if s.endswith('_province'):
        return 'province_definition'
    if s.endswith('_area'):
        return 'area'
    if s.endswith('_region'):
        return 'region'
    if s.endswith('_sub_continent'):
        return 'sub_continent'
    return 'continent'

class CharterFilterGenerator:
    def __init__(self, filepath: str):
        with open(filepath) as file:
            self.parsed: dict = yaml.safe_load(file)
            self.name = path.basename(filepath)[:-4]
            self.tags = self.parsed.get('tags') or []

    def get_enabled_filter(self):
        tag_filters = []
        geo_filters = []
        print(f'loading data for `{self.name}` using the following tags: {', '.join(self.tags)}...')

        for tag in self.tags:
            tag_filters.append(ColonizeEnabled.TAG_TEMPLATE.format(tag=tag))

        if self.parsed.get('charters'):
            charters: dict[int, list[str]] = self.parsed['charters']
            geo_filters.append(self._generate_filters(charters))

        enabled = ColonizeEnabled.FILTER_TEMPLATE.format(
            comment=self.name,
            tags = ''.join(tag_filters).rstrip(),
            geo_filters = ''.join(geo_filters).rstrip()
        )

        return enabled
    
    def _generate_filters(self, charters: dict[int, list[str]] | None) -> str:
        if not charters or len(charters) == 0: return ''
        data = ''
        for year, geographies in charters.items():
            for geography in geographies:
                data += ColonizeEnabled.GEO_FILTER_TEMPLATE.format(
                    year = year,
                    geography_type = get_geography_type(geography),
                    geography = geography
                )
        return data