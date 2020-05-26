from logzero import logger


class Immoweb:

    def __init__(self):
        self.base_url = "http://www/immoweb.be"

    @staticmethod
    def hello_world():
        logger.info("Hello world!")

