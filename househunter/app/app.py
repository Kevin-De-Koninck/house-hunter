import sys
from logzero import logger
from .source_sites.immoweb import Immoweb
from .helpers.helpers import Scraper


class Househunter:
    def __init__(self, settings):
        self.settings = settings.househunter
        self.scraper = Scraper()

        # This will be loaded from and saved to disk
        # It's a list of Residence instances of all residences on all immo websites
        self.all_parsed_residences = []

        # The following vars are mainly used to send notifications
        # They must be provided by each site parser too.

        # This list contains all residences that have a price change since last parsing
        # They will be collected in this list, and the price change will also be added
        # in the self.all_parsed_residences list
        self.all_residences_with_price_changes = []

        # This list contains all new residences that have been added since the last parsing
        # They have been added to self.all_parsed_residences too
        self.all_new_parsed_residences = []

    def parse_all_sites(self):
        for site in self.settings.websites:
            site_class = None
            if site == 'immoweb':
                site_class = Immoweb
            else:
                logger.error("Website '%s' is not a valid website...", site)
                sys.exit(1)

            logger.info("Now parsing all residences on immo site: %s", site)

            # Get all already parsed residences for the chosen site
            all_site_parsed_residences = [r for r in self.all_parsed_residences if r.meta.immo_site == site]

            # Parse them
            site_instance = site_class(self.settings, self.scraper, all_site_parsed_residences)
            site_instance.parse()

            # Remove all previous residences for the chosen site
            self.all_parsed_residences = [r for r in self.all_parsed_residences if r.meta.immo_site != site]

            # Add all new residences for the chosen site
            self.all_parsed_residences += site_instance.all_parsed_residences

            # Remember which one had a price update and all new ones
            self.all_residences_with_price_changes += site_instance.all_residences_with_price_changes
            self.all_new_parsed_residences = site_instance.all_new_parsed_residences

            logger.info("'%s' had %d new residences and %d residences with a price change",
                        site,
                        len(site_instance.all_new_parsed_residences),
                        len(site_instance.all_residences_with_price_changes))

    # Return a list of residences that meet our filter
    def filter_all_new_parsed_results(self):
        passed = [] 

        for residence in self.all_new_parsed_residences:
            s = self.settings.types
            r = residence.meta
            if s.new_real_estate == False and r.new_real_estate == True:
                continue

            s = self.settings.filters.general
            r = residence.general
            if r.facades is not None and s.facades_minimum > r.facades:
                continue
            if r.outdoor_parking_spaces is not None and s.outdoor_parking_spaces_minimum > r.outdoor_parking_spaces:
                continue
            if r.covered_parking_spaces is not None and s.covered_parking_spaces_minimum > r.covered_parking_spaces:
                continue
            if r.construction_year is not None and s.construction_year_minimum > r.construction_year:
                continue
            if r.building_condition is not None:
                if s.exclude_building_condition is not None or 'None' not in s.exclude_building_condition:
                    if r.building_condition in s.exclude_building_condition:
                        continue
                if s.building_condition is not None or 'None' not in s.building_condition:
                    if r.building_condition not in s.exclude_building_condition:
                        continue

            s = self.settings.filters.interior
            r = residence.interior
            if r.kitchen_type is not None:
                if s.exclude_kitchen_type is not None or 'None' not in s.exclude_kitchen_type:
                    if r.kitchen_type in s.exclude_kitchen_type:
                        continue
                if s.kitchen_type is not None or 'None' not in s.kitchen_type:
                    if r.kitchen_type not in s.exclude_kitchen_type:
                        continue
            if r.bedrooms is not None and s.bedrooms_minimum > r.bedrooms:
                continue
            if r.bathrooms is not None and s.bathrooms_minimum > r.bathrooms:
                continue
            if r.toilets is not None and s.toilets_minimum > r.toilets:
                continue
            if r.basement is not None and (r.basement == False and s.has_basement == True):
                continue
            if r.attic is not None and (r.attic == False and s.has_attic == True):
                continue
            if r.furnished is not None and (r.furnished == False and s.is_furnished == True):
                continue

            s = self.settings.filters.exterior
            r = residence.exterior
            if r.surface_of_the_plot is not None and s.surface_of_the_plot_minimum > r.surface_of_the_plot:
                continue
            if r.connected_to_the_sewer_network is not None and (r.is_connected_to_the_sewer_network == False and s.connected_to_the_sewer_network == True):
                continue
            if r.terrace is not None and (r.terrace == False and s.has_terrace == True):
                continue
            if r.has_gas_water_electricity is not None and (r.has_gas_water_electricity == False and s.has_gas_water_electricity == True):
                continue

            s = self.settings.filters.energy
            r = residence.energy
            if r.energy_class is not None and s.energy_class_maximum > r.energy_class:
                continue
            if r.epc is not None and s.epc_maximum < r.epc:
                continue
            if r.double_glazing is not None and (r.double_glazing == False and s.has_double_glazing == True):
                continue
            if r.heat_pump is not None and (r.heat_pump == False and s.has_heat_pump == True):
                continue
            if r.pv_cells is not None and (r.pv_cells == False and s.has_pv_cells == True):
                continue

            s = self.settings.filters.townplanning
            r = residence.townplanning
            if r.flood_zone is not None and (r.flood_zone == True and s.is_flood_zone == False):
                continue
            if r.planning_permission_obtained is not None and (r.planning_permission_obtained == False and s.has_planning_permission_obtained == True):
                continue
            if r.latest_land_use_designation is not None and s.latest_land_use_designation != r.latest_land_use_designation:
                continue

            passed.append(residence)

        logger.info("There were %d new residences found, of which %d meet the requirements", len(self.all_new_parsed_residences), len(passed))
        return passed



