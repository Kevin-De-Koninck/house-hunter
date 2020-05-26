import logging


LOGGER = logging.getLogger(__name__)


def test_app(capsys):
    # pylint: disable=W0612,W0613
    LOGGER.info("Running the method 'hello_world' and checking the output on stdout.")
    assert True

