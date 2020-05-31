import pickle  # nosec
from logzero import logger
from .app.app import Househunter
from .app.settings.settings import Settings
from .app.helpers.pushover import Pushover, Message


def save_app(data, filename):
    with open(filename, 'wb+') as output_stream:
        pickle.dump(data, output_stream, pickle.HIGHEST_PROTOCOL)


def load_app(filename):
    try:
        with open(filename, 'rb') as input_stream:
            data = pickle.load(input_stream)  # nosec
            return data if data is not None else []
    except Exception:
        return []


if __name__ == '__main__':
    config_file = "/app/househunter/resources/config.yml"
    demo_image = "/app/househunter/resources/demo_image.jpg"
    save_data_file = "/app/househunter/resources/save_data.pkl"

    # Parse all settings
    logger.debug("Parsing all settings from file: %s", config_file)
    settings = Settings(config_file)

    # Load app or start clean
    logger.debug("Loading all data from save file: %s", save_data_file)
    househunter = Househunter(settings)
    househunter.all_parsed_residences = load_app(save_data_file)

    # Run the actual app
    logger.debug("Running the actual app now....")
    househunter.parse_all_sites()

    # Save the data for a next run
    logger.debug("Saving all data to save file: %s", save_data_file)
    save_app(househunter.all_parsed_residences, save_data_file)

    # Pushover
    p = Pushover(settings.pushover.user_key, settings.pushover.API_token)
    m = Message(title="Fancy title here", message="test message",
                image_path=demo_image, url="www.google.com",
                url_title="My url", priority=Message.HIGH_PRIORITY)
    m.add_message("Added message 1")
    m.add_message("Added message 2")
    # p.send(m)

    logger.info("Successfully parsed all residences")

