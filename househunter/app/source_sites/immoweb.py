from logzero import logger
from bs4 import BeautifulSoup
from copy import deepcopy
from ..models.residence import Residence, General, Interior, Exterior, Energy, Townplanning, Meta


class Search_result_item:
    def __init__(self):
        self.price = None
        self.url = None
        self.reference_code = None
        self.house = False
        self.apartment = False
        self.new_real_estate = False


class Immoweb:
    HOUSE = 'house'
    APARTMENT = 'apartment'
    NEW_REAL_ESTATE_HOUSE = 'new-real-estate-project-houses'
    NEW_REAL_ESTATE_APARTMENT = 'new-real-estate-project-apartments'
    NEW_REAL_ESTATE = 'new-real-estate'

    def __init__(self, settings, scraper, all_parsed_residences):
        self.settings = settings
        self.scraper = scraper
        self.base_url = "http://www.immoweb.be/en/search/{residence}/for-sale?" \
                        "countries=BE&minPrice={min_price}&maxPrice={max_price}" \
                        "&minBedroomCount={min_bedrooms}&orderBy=relevance" \
                        "&postalCodes=BE-{postal_codes}"

        # A list of Residences already saved on disk from a previous time
        self.all_parsed_residences = all_parsed_residences

        # All search result items in the list, list of class Search_result_item
        self.all_results_in_search = []

        # All results in search that are new items
        # Price changes and residence obsoletions will happen in self.all_results_in_search
        self.all_new_results_in_search = []

        # Remember all instances that had a price update
        self.all_residences_with_price_changes = []

        # Remember all new residences that have been added
        self.all_new_parsed_residences = []

    def parse(self):
        residence_types = []
        if self.settings.types.house == True:
            residence_types.append(self.HOUSE)
        if self.settings.types.apartment == True:
            residence_types.append(self.APARTMENT)
        if self.settings.types.new_real_estate == True and self.settings.types.house == True:
            residence_types.append(self.NEW_REAL_ESTATE_HOUSE)
        if self.settings.types.new_real_estate == True and self.settings.types.apartment == True:
            residence_types.append(self.NEW_REAL_ESTATE_APARTMENT)

        for residence_type in residence_types:
            logger.debug("Now parsing the search results for residence type: %s", residence_type)
            base_search_url = self.create_base_search_url(residence_type)
            self.get_all_search_result_links(base_search_url, residence_type)

        self.determine_new_deleted_and_changed_results()
        self.parse_search_results()

    def determine_new_deleted_and_changed_results(self):
        all_found_reference_codes = [i.reference_code for i in self.all_results_in_search]

        # Determine deleted and delete them from the list
        logger.debug("Determing and deleting all deleted residences from our data based on the search results")
        self.all_parsed_residences = [r for r in self.all_parsed_residences if r.meta.reference_code in all_found_reference_codes]

        # Determine all residences of which the price has changed
        logger.debug("Determing all resididences that had a price change based on the search results")
        for residence in self.all_parsed_residences:
            matching_search_list_item = [i for i in self.all_results_in_search if i.reference_code == residence.meta.reference_code][0]

            # If the price did not change, do nothing
            if matching_search_list_item.price == residence.meta.price.price:
                continue

            # Delete the old match from the list
            self.all_parsed_residences = [r for r in self.all_parsed_residences if r != residence]

            # Update the price with the new price from the list
            new_residence = deepcopy(residence)
            new_residence.meta.price.add(matching_search_list_item.price)

            # Add the new residence with updated price
            self.all_parsed_residences.append(new_residence)
            self.all_residences_with_price_changes.append(new_residence)
        logger.debug("The following residences had a price change: %s", repr([r.meta.reference_code for r in self.all_residences_with_price_changes]))

        # Determine all new residences
        all_existing_reference_codes = [r.meta.reference_code for r in self.all_parsed_residences]
        self.all_new_results_in_search = [i for i in self.all_results_in_search if i.reference_code not in all_existing_reference_codes]
        logger.debug("The following residences are new and will be parsed: %s", ', '.join([i.reference_code for i in self.all_new_results_in_search]))

    def create_base_search_url(self, property_type):
        data = {}
        data['postal_codes'] = "%2C".join([str(i) for i in self.settings.postal_codes])
        if self.NEW_REAL_ESTATE in property_type:
            data['min_price'] = self.settings.price.new_real_estate.minimum
            data['max_price'] = self.settings.price.new_real_estate.maximum
        else:
            data['min_price'] = self.settings.price.old_real_estate.minimum
            data['max_price'] = self.settings.price.old_real_estate.maximum
        data['residence'] = property_type
        data['min_bedrooms'] = self.settings.filters.interior.bedrooms_minimum
        url = self.base_url.format(**data)
        logger.debug("Using the following url: %s", url)
        return url

    def get_all_search_result_links(self, base_search_url, residence_type):
        pages = [base_search_url]

        for page in pages:
            logger.debug("Parsing search results on page: %s", page)
            p = BeautifulSoup(self.scraper.get_page(page), 'html.parser')

            list_of_search_items = p.find("ul", id="main-content")
            all_list_items = list_of_search_items.find_all('li', class_="search-results__item")
            for item in all_list_items:
                # Get the first link
                try:
                    a = item.find_all('a')[0]
                except (IndexError, TypeError):
                    continue

                # Skip sponsored items
                if "adfocus" in ''.join(a.get('class')):
                    continue

                # Get all data from each search result
                search_result = Search_result_item()
                price_string = item.find('p', class_='card--result__price').find('span', class_='sr-only').text.strip()
                search_result.price = int(''.join(filter(str.isdigit, price_string)))
                search_result.url = a.get('href')
                search_result.reference_code = a.get('href').split('/')[-1].split('?')[0]

                # Remember the type
                if residence_type == self.HOUSE:
                    search_result.house = True
                if residence_type == self.APARTMENT:
                    search_result.apartment = True
                if residence_type == self.NEW_REAL_ESTATE_HOUSE:
                    search_result.new_real_estate = True
                    search_result.house = True
                if residence_type == self.NEW_REAL_ESTATE_APARTMENT:
                    search_result.new_real_estate = True
                    search_result.apartment = True

                self.all_results_in_search.append(search_result)

            # If we have multiple pages, save the link of the next page
            try:
                next_page = p.find('a', class_='pagination__link--next').get('href')
                pages.append(next_page)
            except AttributeError:
                pass

        logger.debug("There were %d search results returned and parsed", len(self.all_results_in_search))

    def parse_search_results(self):
        all_residences = []
        logger.debug("Parsing all new search results")
        for search_result in self.all_new_results_in_search:
            logger.debug("Parsing residence with reference code: %s", str(search_result.reference_code))

            meta = Meta()
            general = General()
            interior = Interior()
            exterior = Exterior()
            energy = Energy()
            townplanning = Townplanning()

            page = BeautifulSoup(self.scraper.get_page(search_result.url), 'html.parser')

            # Meta
            meta.immo_site = "immoweb"
            price_string = page.find('p', class_='classified__price').find_next('span', class_='sr-only').text.strip()
            meta.price.add(int(''.join(filter(str.isdigit, price_string))))
            meta.reference_code = page.find('div', class_='classified__information--immoweb-code').text.split(':')[1].strip()
            address_line = ' '.join(page.find('div', class_='classified__information--address').find('span').text.split())
            address_line_split = address_line.split('|')
            if len(address_line_split) == 1:  # If an address was specified, this will be True
                spans = page.find('div', class_='classified__information--address').find_all('span')
                meta.address = ' '.join(spans[0].text.replace('\n', '').split())
                meta.postal_code = spans[2].text.strip()
                meta.city = spans[4].text.strip()
            else:
                meta.postal_code = address_line_split[0].split('—')[0].strip()
                meta.city = address_line_split[0].split('—')[1].strip()
            meta.house = search_result.house
            meta.apartment = search_result.apartment
            meta.new_real_estate = search_result.new_real_estate

            # General secition
            try:
                general.residence_type = page.find('h1', class_='classified__title').text.replace('for sale', '').strip()
                general_section = page.find('h2', class_='text-block__title', string='General').find_next('tbody').find_all('tr')
            except AttributeError:
                general_section = []
            for line in general_section:
                key = line.find('th').text.strip().lower()
                value = line.find('td').text.strip()
                if key == 'available as of':
                    general.available_as_of = value
                elif key == 'construction year':
                    general.construction_year = value
                elif key == 'building condition':
                    general.building_condition = value
                elif key == 'facades':
                    general.facades = value
                elif key == 'covered parking spaces':
                    general.covered_parking_spaces = value
                elif key == 'outdoor parking spaces':
                    general.outdoor_parking_spaces = value
                elif key == 'street facade width':
                    general.facade_width_street = value
                elif key == 'floor':
                    general.floor = value
                elif key == 'number of floors':
                    general.number_of_floors = value

            # Interior section
            try:
                interior_section = page.find('h2', class_='text-block__title', string='Interior').find_next('tbody').find_all('tr')
            except AttributeError:
                interior_section = []
            for line in interior_section:
                key = line.find('th').text.strip().lower()
                value = line.find('td').text.strip()
                if key == 'kitchen type':
                    interior.kitchen_type = value
                elif key == 'bedrooms':
                    interior.bedrooms = value
                elif key == 'bathrooms':
                    interior.bathrooms = value
                elif key == 'toilets':
                    interior.toilets = value
                elif key == 'basement':
                    interior.basement = value
                elif key == 'attic':
                    interior.attic = value
                elif key == 'furnished':
                    interior.furnished = value

            # Exterior section
            try:
                exterior_section = page.find('h2', class_='text-block__title', string='Exterior').find_next('tbody').find_all('tr')
            except AttributeError:
                exterior_section = []
            for line in exterior_section:
                key = line.find('th').text.strip().lower()
                value = line.find('td').text.strip()
                if key == 'surface of the plot':
                    interior.surface_of_the_plot = value.split()[0]
                elif key == 'connection to sewer network':
                    interior.connected_to_the_sewer_network = value
                elif key == 'terrace':
                    interior.terrace = value
                elif key == 'gas, water & electricity':
                    interior.has_gas_water_electricity = value

            # Energy section
            try:
                energy_section = page.find('h2', class_='text-block__title', string='Energy').find_next('tbody').find_all('tr')
            except AttributeError:
                energy_section = []
            for line in energy_section:
                key = line.find('th').text.strip().lower()
                try:
                    value = line.find('td').text.strip()
                except AttributeError:  # Energy class image
                    continue
                if 'e-level' in key:
                    energy.epc = value
                elif key == 'energy class':
                    energy.energy_class = value
                elif key == 'heating type':
                    energy.heating_type = value
                elif key == 'double glazing':
                    energy.double_glazing = value
                elif key == 'heat pump':
                    energy.heat_pump = value
                elif 'solar panels' in key:
                    energy.pv_cells = value

            # townplanning section
            try:
                townplanning_section = page.find('h2', class_='text-block__title', string='Town planning').find_next('tbody').find_all('tr')
            except AttributeError:
                townplanning_section = []
            for line in townplanning_section:
                key = line.find('th').text.strip().lower()
                value = line.find('td').text.strip()
                if 'flood zone' in key:
                    townplanning.flood_zone = value
                elif key == 'latest land use designation':
                    townplanning.Latest_land_use_designation = value
                elif key == 'planning permission obtained':
                    townplanning.planning_permission_obtained = value

            # Create a residence
            residence = Residence(general=general, interior=interior, exterior=exterior, energy=energy, townplanning=townplanning, meta=meta)
            all_residences.append(residence)

        # Add the new results
        logger.debug("there were %d new residences parsed", len(all_residences))
        self.all_new_parsed_residences += all_residences
        self.all_parsed_residences += all_residences

