import sys
import requests
from logzero import logger


class Pushover:
    def __init__(self, user_key, project_api_token):
        self.user_key = user_key
        self.project_api_token = project_api_token

    def send_notification(self, message, image_path=None):
        files = {}
        if image_path is not None:
            files = {"attachment": ("image.jpg", open(image_path, "rb"), "image/jpeg")}

        logger.debug("Sending push notification with the following message:\n%s", message)
        response = requests.post("https://api.pushover.net/1/messages.json",
                                 data={"token": self.project_api_token,
                                       "user": self.user_key,
                                       "message": message},
                                 files=files)

        if response.status_code == 200:
            logger.debug("Successfully sent the push notification.")
        else:
            logger.error("Unable to send a push notification. The full return was:\n%s", repr(response.__dict__))
            sys.exit(1)

    def send(self, message_object):
        self.send_notification(message_object.message, message_object.image_path)


class Pushover_message:
    def __init__(self, message="", image_path=None):
        self.message = message
        self.image_path = image_path

    def add_message(self, message):
        self.message += message + "\n"

    def add_image(self, image_path):
        self.image_path = image_path

