import yaml
from os import path
from templates import *
from templates.take_location import TakeLocation
from templates.colonize_province import ColonizeProvince
from templates.colonize_in_area import ColonizeInArea
from templates.colonize_in_region import ColonizeInRegion

class ColonyEventGenerator:
    def __init__(self, filepath: str):
        with open(filepath) as file:
            self.parsed: dict = yaml.safe_load(file)

            self.tag, self.name = path.basename(filepath)[:-4].split('_')
            self.other_tags = self.parsed.get('tags') or []

    def write_all(self, event_out: str, localization_out: str):
        file_data = []

        file_data.append(self._generate_files(TakeLocation, self.parsed.get('locations')))
        file_data.append(self._generate_files(ColonizeProvince, self.parsed.get('provinces')))
        file_data.append(self._generate_files(ColonizeInArea, self.parsed.get('areas')))
        file_data.append(self._generate_files(ColonizeInRegion, self.parsed.get('regions')))

        # write events
        for data in file_data:
            if not data: continue
            with open(path.join(event_out, f'{data['namespace']}.txt'), 'w', encoding='utf-8-sig') as file:
                file.write(data['event'])
        
        # write localization
        lines = []
        with open(localization_out, 'r', encoding='utf-8-sig') as file:
            lines = file.read().split('\n')

            # add l_english if not present
            if len(lines) == 0:
                lines.append('l_english:')
            if len(lines) > 0 and 'l_english' not in lines[0]:
                lines.insert(0, 'l_english:')

            existing_loc_keys = [loc_line.split(':')[0].strip() for loc_line in lines[1:]]
            for data in file_data:
                if not data: continue
                for loc_line in data['localization'].split('\n'):
                    key = loc_line.split(':')[0].strip()
                    if (key not in existing_loc_keys):
                        lines.append(loc_line)
        
        if len(lines) > 0:
            with open(localization_out, 'w', encoding='utf-8-sig') as file:
                for line in lines:
                    if len(line) > 0:
                        file.write(line+'\n')

    def _parse_year(self, year: str | int, fallback_range=4) -> list:
        if type(year) == int:
            return [year-fallback_range, year+fallback_range]
        else:
            return str(year).replace(' ', '').split('-')

    def _generate_files(self, template: type[TemplateData], geo: dict[str, str] | None) -> dict[str, str]:
        if not geo or len(geo) == 0: return {}
        namespace = template.NAMESPACE.format(name=self.name)

        data = {
            'localization': '',
            'namespace': namespace,
            'event': f'namespace = {namespace}\n\n',
        }
        for index, (geography, year) in enumerate(geo.items()):
            from_year, to_year = self._parse_year(year)
            data['localization'] += template.LOCALIZATION_TEMPLATE.format(
                n = index+1,
                name = self.name.strip()
            )
            data['event'] += template.EVENT_TEMPLATE.format(
                tags = make_tags([self.tag] + self.other_tags),
                name = self.name.strip(),
                n = index+1,
                from_year = from_year,
                to_year = to_year,
                geography = geography.strip()
            )
        return data