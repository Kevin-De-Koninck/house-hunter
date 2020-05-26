import sys
import requests
from logzero import logger


class Pushover:
    def __init__(self, user_key, project_api_token):
        self.user_key = user_key
        self.project_api_token = project_api_token

    def send(self, message):
        files = {}
        data = {}

        data['token'] = self.project_api_token
        data['user'] = self.user_key
        data['message'] = message.message
        data['priority'] = message.priority
        if message.title is not None:
            data['title'] = message.title
        if message.url is not None:
            data['url'] = message.url
        if message.url_title is not None:
            data['url_title'] = message.url_title
        if message.image_path is not None:
            files = {"attachment": ("image.jpg", open(message.image_path, "rb"), "image/jpeg")}
        

        logger.debug("Sending push notification with the following message:\n%s", message)
        response = requests.post("https://api.pushover.net/1/messages.json",
                                 data=data,
                                 files=files)

        if response.status_code == 200:
            logger.debug("Successfully sent the push notification.")
        else:
            logger.error("Unable to send a push notification. The full return was:\n%s", repr(response.__dict__))
            sys.exit(1)


class Message:
    NO_NOTIFICATION = -2
    QUIET_NOTIFICATION = -1
    NORMAL_NOTIFICATION = 0
    HIGH_PRIORITY = 1

    def __init__(self, title=None, message="", image_path=None, url=None, url_title=None, priority=None):
        self.title = title
        self.message = message
        self.image_path = image_path
        self.url = url
        self.url_title = url_title
        self.priority = self.NORMAL_NOTIFICATION if priority is None else priority

    def __str__(self):
        return repr(self.__dict__)

    def add_message(self, message):
        if self.message != "":
            self.message += "\n"
        self.message += message + "\n"


