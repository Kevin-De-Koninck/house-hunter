import argparse
import pickle  # nosec
from ast import literal_eval
from yaml import dump
from sys import exit
from logzero import logger
from .app.app import Househunter
from .app.settings.settings import Settings
from .app.helpers.pushover import Pushover, Message


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset-data",
                        action="store_true", default=False,
                        help="Reset all data and recreate it. This will parse all results again and might take a while.")
    parser.add_argument("--apply-filters-only",
                        action="store_true", default=False,
                        help="Do not scan for new plots, just apply the filters on the existing data again.")
    parser.add_argument("--no-notification",
                        action="store_true", default=False,
                        help="Do not send a notification on a match")
    return parser.parse_args()


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

    # Parse arguments
    args = parse_args()
    all_args_str = ""
    if args.reset_data:
        all_args_str += "--reset-data "
    if args.apply_filters_only:
        all_args_str += "--apply-filters-only "
    if args.no_notification:
        all_args_str += "--no-notification "    
    logger.debug('Running with the following arguments: %s', all_args_str)

    # Parse all settings
    logger.debug("Parsing all settings from file: %s", config_file)
    settings = Settings(config_file)

    # Load app or start clean
    logger.debug("Loading all data from save file: %s", save_data_file)
    househunter = Househunter(settings)
    if not args.reset_data:
        househunter.all_parsed_residences = load_app(save_data_file)

    # Run the actual app
    logger.debug("Running the actual app now....")
    if not args.apply_filters_only:
        househunter.parse_all_sites()

    # Save the data for a next run
    logger.debug("Saving all data to save file: %s", save_data_file)
    save_app(househunter.all_parsed_residences, save_data_file)

    # Check all new results for filter matches
    if args.apply_filters_only:
        househunter.all_new_parsed_residences = househunter.all_parsed_residences
    matches = househunter.filter_all_new_parsed_results()

    # Create a pushover instance to send notifications
    pushover = Pushover(settings.pushover.user_key, settings.pushover.API_token)

    # For each new passed residence, send a notification
    for residence in matches:
        if args.no_notification:
            logger.info("The following residence matched all filters: %s", repr(residence))
        else:
            logger.debug("Sending a notification for new residence '%s' on '%s'", residence.meta.reference_code, residence.meta.immo_site)
            message = Message(title='New: {} - {}'.format(residence.meta.reference_code, residence.meta.immo_site),
                              url=residence.meta.url,
                              priority=Message.NORMAL_NOTIFICATION,
                              image_path=demo_image,
                              image_base64=residence.meta.image)
            message.add_message("Price: {:,.2f}".format(int(residence.meta.price.price)))
            message.add_message("Location: {} - {}".format(residence.meta.postal_code, residence.meta.city))
            pushover.send(message)

    # For each price change, send a notification
    for residence in househunter.all_residences_with_price_changes:
        if args.no_notification:
            logger.info("The following residences had a price change: %s", repr(residence))
        else:
            logger.debug("Sending a notification for price changed residence '%s' on '%s'", residence.meta.reference_code, residence.meta.immo_site)
            message = Message(title='PRICE CHANGE: {} - {}'.format(residence.meta.reference_code, residence.meta.immo_site),
                              url=residence.meta.url,
                              priority=Message.HIGH_PRIORITY,
                              image_path=demo_image,
                              image_base64=residence.meta.image)
            message.add_message("Price: {:,.2f}".format(int(residence.meta.price.price)))
            message.add_message("Location: {} - {}".format(residence.meta.postal_code, residence.meta.city))
            message.add_message("")
            message.add_message("PRICE CHANGES:")
            message.add_message("")
            message.add_message(dump(literal_eval(repr(residence.meta.price)), default_flow_style=False))
            pushover.send(message)

    # The end
    logger.info("Successfully parsed all residences")
    exit(0)

