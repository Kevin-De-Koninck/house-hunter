import argparse
from logzero import logger
from .app.app import Househunter
from.app.settings import Settings, Pushover_settings, Househunter_settings

if __name__ == '__main__':
    config_file = "/app/househunter/resources/config.yml"

    settings = Settings(config_file)
    ps = Pushover_settings(config_file)
    hs = Househunter_settings(config_file)

    logger.debug("The API_key: {}".format(settings.pushover.API_token))
    logger.debug("The API_key: {}".format(ps.API_token))

    logger.debug("The enabled_sites: {}".format(settings.househunter.enabled_sites))
    logger.debug("The enabled_sites: {}".format(hs.enabled_sites))

    logger.debug("The old_realestate price maximum: {}".format(settings.househunter.price.old_real_estate.maximum))
    logger.debug("The old_realestate price maximum: {}".format(hs.price.old_real_estate.maximum))

    logger.debug("The property types: {}".format(settings.househunter.property.types))
    logger.debug("The property types: {}".format(hs.property.types))

    logger.debug("The property required bedrooms min: {}".format(settings.househunter.property.filters.required.bedrooms_min))
    logger.debug("The property required bedrooms min: {}".format(hs.property.filters.required.bedrooms_min))

    print(repr(ps.__dict__))
