import sys
import requests
from logzero import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Anon_kwargs:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Anon_dict:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, dict):
                setattr(self, k, Anon_dict(v))
            else:
                setattr(self, k, v)


class Helpers:
    # Much faster (but simpler) deepcopy implementation that is sufficient for the needs of this script
    @staticmethod
    def deepcopy(original):
        new = dict().fromkeys(original)
        for k, v in original.items():
            try:
                new[k] = v.copy()  # dicts, sets
            except AttributeError:
                try:
                    new[k] = v[:]  # lists, tuples, strings, unicode
                except TypeError:
                    new[k] = v  # int
        return new

    @staticmethod
    def convert_to_value(yaml_expression, dictionary):
        value = Helpers.deepcopy(dictionary)
        try:
            for key in yaml_expression.split('.'):
                value = value[key]
                if value is None:
                    break
        except (AttributeError, KeyError):
            logger.error("Key '%s' does not exist in the following dictionary:\n%s'",
                         yaml_expression, repr(dictionary))
            sys.exit(1)
        return value


class Scraper:
    def __init__(self):
        self.browser = self.init_browser()

    @staticmethod
    def init_browser():
        options = Options()
        options.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.http.pipelining", True)
        profile.set_preference("network.http.proxy.pipelining", True)
        profile.set_preference("network.http.pipelining.maxrequests", 8)
        profile.set_preference("content.notify.interval", 500000)
        profile.set_preference("content.notify.ontimer", True)
        profile.set_preference("content.switch.threshold", 250000)
        # Increase the cache capacity
        profile.set_preference("browser.cache.memory.capacity", 65536)
        profile.set_preference("browser.startup.homepage", "about:blank")
        # Disable reader, we won't need that
        profile.set_preference("reader.parse-on-load.enabled", False)
        # Duck pocket too
        profile.set_preference("browser.pocket.enabled", False)
        profile.set_preference("loop.enabled", False)
        # Text on Toolbar instead of icons
        profile.set_preference("browser.chrome.toolbar_style", 1)
        # Don't show thumbnails on not loaded images
        profile.set_preference("browser.display.show_image_placeholders", False)
        # Don't show document colors
        profile.set_preference("browser.display.use_document_colors", False)
        # Don't load document fonts
        profile.set_preference("browser.display.use_document_fonts", 0)
        # Use system colors
        profile.set_preference("browser.display.use_system_colors", True)
        # Autofill on forms disabled
        profile.set_preference("browser.formfill.enable", False)
        # Delete temprorary files
        profile.set_preference("browser.helperApps.deleteTempFileOnExit", True)
        profile.set_preference("browser.shell.checkDefaultBrowser", False)
        profile.set_preference("browser.startup.homepage", "about:blank")
        profile.set_preference("browser.startup.page", 0)
        # Disable tabs, We won't need that
        profile.set_preference("browser.tabs.forceHide", True)
        # Disable autofill on URL bar
        profile.set_preference("browser.urlbar.autoFill", False)
        # Disable autocomplete on URL bar
        profile.set_preference("browser.urlbar.autocomplete.enabled", False)
        # Disable list of URLs when typing on URL bar
        profile.set_preference("browser.urlbar.showPopup", False)
        # Disable search bar
        profile.set_preference("browser.urlbar.showSearch", False)
        # Addon update disabled
        profile.set_preference("extensions.checkCompatibility", False)
        profile.set_preference("extensions.checkUpdateSecurity", False)
        profile.set_preference("extensions.update.autoUpdateEnabled", False)
        profile.set_preference("extensions.update.enabled", False)
        profile.set_preference("general.startup.browser", False)
        profile.set_preference("plugin.default_plugin_disabled", False)
        # Image load disabled again
        profile.set_preference("permissions.default.image", 2)
        # Disable CSS
        profile.set_preference('permissions.default.stylesheet', 2)
        # Disable flash
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        # Use ublock extension
        profile.add_extension(extension='/app/househunter/resources/ublock.xpi')
        # Use noscript extension
        profile.add_extension(extension='/app/househunter/resources/noscript.xpi')
        return webdriver.Firefox(options=options, firefox_profile=profile)

    def get_page(self, url, javascript_enabled_website=True):
        page = None
        if javascript_enabled_website:
            self.browser.get(url)
            page = self.browser.page_source
            return self.browser.page_source

        try:
            page = requests.get(url)
            if page.status_code != 200:
                logger.error("Unable to retrieve page (returncode != 200):\n%s", url)
                sys.exit(1)
        except requests.exceptions.InvalidSchema as e:
            logger.error("Unable to retrieve page:\n%s", url)
            logger.exception(e)
            sys.exit(-1)
        return page

