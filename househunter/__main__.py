from logzero import logger
from .app.app import Househunter
from.app.settings import Settings, Pushover_settings, Househunter_settings

if __name__ == '__main__':
    config_file = "/app/househunter/resources/config.yml"

    h = Househunter()

    settings = Settings(config_file)
    ps = Pushover_settings(config_file)
    hs = Househunter_settings(config_file)

    logger.debug("The API_key: %s", settings.pushover.API_token)
    logger.debug("The API_key: %s", ps.API_token)

    logger.debug("The enabled_sites: %s", settings.househunter.enabled_sites)
    logger.debug("The enabled_sites: %s", hs.enabled_sites)

    logger.debug("The old_realestate price maximum: %s", settings.househunter.price.old_real_estate.maximum)
    logger.debug("The old_realestate price maximum: %s", hs.price.old_real_estate.maximum)

    logger.debug("The property types: %s", settings.househunter.property.types)
    logger.debug("The property types: %s", hs.property.types)

    logger.debug("The property required bedrooms min: %s", settings.househunter.property.filters.required.bedrooms_min)
    logger.debug("The property required bedrooms min: %s", hs.property.filters.required.bedrooms_min)

