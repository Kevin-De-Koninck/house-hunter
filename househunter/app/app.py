import sys
from logzero import logger
from .source_sites.immoweb import Immoweb
from .models.posting import Posting


class Househunter:

    def __init__(self, settings):
        self.hs = settings.househunter
        self.ps = settings.pushover

        print(self.hs.websites)

    def parse_all_sites(self):
        for site in self.hs.websites:
            site_class = None
            if site == 'immoweb.be':
                site_class = Immoweb
            else:
                logger.error("Website '%s' is not a valid website...", site)
                sys.exit(1)
            self.parse_site(site_class(self.hs))

    def parse_site(self, site):
        _ = self.hs
        site.hello_world()

    def hello_world(self):
        print(repr(Posting().__dict__))
        print(repr(Posting().residence.__dict__))
        Immoweb(self.hs).hello_world()
        Immoweb(self.hs).parse()
