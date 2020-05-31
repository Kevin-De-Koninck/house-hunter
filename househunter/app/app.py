import sys
from logzero import logger
from .source_sites.immoweb import Immoweb
from .helpers.helpers import Scraper


class Househunter:
    def __init__(self, settings):
        self.hs = settings.househunter
        self.ps = settings.pushover
        self.scraper = Scraper()
        self.all_parsed_residences = []
        self.all_residences_with_price_changes = []
        self.all_new_parsed_residences = []

    def parse_all_sites(self):
        for site in self.hs.websites:
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
            site_instance = site_class(self.hs, self.scraper, all_site_parsed_residences)
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

