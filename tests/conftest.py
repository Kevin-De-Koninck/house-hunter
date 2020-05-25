import logging
import pytest
from .context import Househunter


LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def househunter_object():
    LOGGER.info("Initializing the module and returning the object...")
    yield Househunter()
    LOGGER.info("Breaking down the module.")
    # Do clean up here

