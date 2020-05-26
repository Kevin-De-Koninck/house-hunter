import os
import sys
import yaml
from logzero import logger
from .helpers import Helpers, Micro_mock


class Config_file_parser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.check_if_file_exists()

    def check_if_file_exists(self):
        if not os.path.exists(self.config_file):
            logger.error("File '%s' does not exist...", self.config_file)
            sys.exit(1)
        if not os.path.isfile(self.config_file):
            logger.error("Path '%s' is not a file...", self.config_file)
            sys.exit(1)

    def parse_yaml(self):
        results = {}
        with open(self.config_file, 'r') as stream:
            try:
                results = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error("Error while parsing YAML file '%s':\n%s", self.config_file, exc)
                sys.exit(1)
        return results


class Settings:
    def __init__(self, config_file):
        self.settings_dict = Config_file_parser(config_file).parse_yaml()

    def convert_to_value(self, yaml_expression):
        return Helpers.convert_to_value(yaml_expression, self.settings_dict)


class Pushover_settings(Settings):
    def __init__(self, config_file):
        super().__init__(config_file)
        self.API_key = self.get_value('API_token')
        self.user_key = self.get_value('user_key')

    def get_value(self, key):
        return self.convert_to_value('pushover.{}'.format(key))


class Househunter_settings(Settings):
    def __init__(self, config_file):
        super().__init__(config_file)
        self.enabled_sites = self.get_value('enabled_sites')
        self.postal_codes = self.get_value('postal_codes')
        self.price = self.create_price_object()
        self.property = self.create_property_object()        

    def get_value(self, key):
        return self.convert_to_value('househunter.{}'.format(key))

    def create_price_object(self):
        old_realestate = Micro_mock(minimum=self.get_value('price.old_real_estate.minimum'),
                                    maximum=self.get_value('price.old_real_estate.maximum'))
        new_realestate = Micro_mock(minimum=self.get_value('price.new_real_estate.minimum'),
                                    maximum=self.get_value('price.new_real_estate.maximum'))
        return Micro_mock(old_realestate=old_realestate, new_realestate=new_realestate)

    def create_property_object(self):
        types = self.get_value('property.types')
        filters = self.create_filters_object()
        return Micro_mock(types=types, filters=filters)

    def create_filters_object(self):
        required = self.create_required_filters_object()
        preferred = self.create_preferred_filters_object()
        return Micro_mock(required=required, preferred=preferred)

    def create_required_filters_object(self):
        bedrooms_min = self.get_value('property.filters.required.bedrooms_min')
        connected_to_the_sewer_network = self.get_value('property.filters.required.connected_to_the_sewer_network')
        flood_zone = self.get_value('property.filters.required.flood_zone')
        gas_water_electricity = self.get_value('property.filters.required.gas_water_electricity')
        double_glazing = self.get_value('property.filters.required.double_glazing')
        planning_permission_obtained = self.get_value('property.filters.required.planning_permission_obtained')
        Latest_land_use_designation = self.get_value('property.filters.required.Latest_land_use_designation')
        epc_max = self.get_value('property.filters.required.epc_max')
        build_year_max = self.get_value('property.filters.required.build_year_max')
        return Micro_mock(bedrooms_min=bedrooms_min,
                          connected_to_the_sewer_network=connected_to_the_sewer_network,
                          flood_zone=flood_zone,
                          gas_water_electricity=gas_water_electricity,
                          double_glazing=double_glazing,
                          planning_permission_obtained=planning_permission_obtained,
                          Latest_land_use_designation=Latest_land_use_designation,
                          epc_max=epc_max,
                          build_year_max=build_year_max)

    def create_preferred_filters_object(self):
        building_state = self.get_value('property.filters.preferred.building_state')
        kitchen_type = self.get_value('property.filters.preferred.kitchen_type')
        facades = self.get_value('property.filters.preferred.facades')
        mobi_score_min = self.get_value('property.filters.preferred.mobi_score_min')
        garage = self.get_value('property.filters.preferred.garage')
        garden = self.get_value('property.filters.preferred.garden')
        return Micro_mock(building_state=building_state,
                          kitchen_type=kitchen_type,
                          facades=facades,
                          mobi_score_min=mobi_score_min,
                          garage=garage,
                          garden=garden)

