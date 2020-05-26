import argparse
from logzero import logger
from .app.app import Househunter
from.app.settings import Pushover_settings, Househunter_settings

if __name__ == '__main__':
    config_file = "/app/househunter/resources/config.yml"

    p_settings = Pushover_settings(config_file)
    h_settings = Househunter_settings(config_file)

    logger.debug("The API_key: {}".format(p_settings.API_key))
    logger.debug("The enabled_sites: {}".format(h_settings.enabled_sites))
    logger.debug("The old_realestate price maximum: {}".format(h_settings.price.old_realestate.maximum))
    logger.debug("The property types: {}".format(h_settings.property.types))
    logger.debug("The property required bedrooms min: {}".format(h_settings.property.filters.required.bedrooms_min))


