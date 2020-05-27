from logzero import logger
from .app.app import Househunter
from .app.settings.settings import Settings
from .app.helpers.pushover import Pushover, Message

if __name__ == '__main__':
    config_file = "/app/househunter/resources/config.yml"
    demo_image = "/app/househunter/resources/demo_image.jpg"

    settings = Settings(config_file)

    logger.debug("The API_key: %s", settings.pushover.API_token)
    logger.debug("The old_realestate price maximum: %s", settings.househunter.price.old_real_estate.maximum)
    logger.debug("The property types: %s", settings.househunter.property.types)
    logger.debug("The property required bedrooms min: %s", settings.househunter.property.filters.required.bedrooms_min)

    p = Pushover(settings.pushover.user_key, settings.pushover.API_token)
    m = Message(title="Fancy title here", message="test message",
                image_path=demo_image, url="www.google.com",
                url_title="My url", priority=Message.HIGH_PRIORITY)
    m.add_message("Added message 1")
    m.add_message("Added message 2")
    # p.send(m)

    h = Househunter(settings)
    h.parse_all_sites()
    h.hello_world()
