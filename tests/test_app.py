import logging
import pytest


LOGGER = logging.getLogger(__name__)


def test_app(capsys, househunter_object):
    # pylint: disable=W0612,W0613
    LOGGER.info("Running the method 'hello_world' and checking the output on stdout.")
    househunter_object.hello_world()
    captured = capsys.readouterr()
    assert "Hello World" in captured.out


def test_inc(househunter_object):
    # pylint: disable=W0612,W0613
    LOGGER.info("Initializing Househunter class and running the method 'inc'")
    househunter_object.inc()
    assert househunter_object.value == 2


def test_systemerror(capsys, househunter_object):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        househunter_object.raise_systemerror()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    captured = capsys.readouterr()
    assert "Logging info is not captured in pytest." not in captured.out.split("\n")
    assert "Standard print output is captured in pytest." in captured.out.split("\n")

