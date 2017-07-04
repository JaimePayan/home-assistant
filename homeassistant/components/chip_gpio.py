"""
Support for controlling GPIO pins of a CHIP.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/chip_gpio/
"""
# pylint: disable=import-error
import logging

from homeassistant.const import (
    EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP)

REQUIREMENTS = ['CHIP-IO==0.5.9']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'chip_gpio'


# pylint: disable=no-member
def setup(hass, config):
    """Set up the Chip GPIO component."""
    import CHIP_IO.GPIO as GPIO

    def cleanup_gpio(event):
        """Stuff to do before stopping."""
        GPIO.cleanup()

    def prepare_gpio(event):
        """Stuff to do when home assistant starts."""
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup_gpio)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare_gpio)
    #GPIO.setmode(GPIO.BCM)
    return True


def setup_output(port):
    """Set up a GPIO as output."""
    import CHIP_IO.GPIO as GPIO
    GPIO.setup(port, GPIO.OUT)


def setup_input(port, pull_mode):
    """Set up a GPIO as input."""
    import CHIP_IO.GPIO as GPIO
    GPIO.setup(port, GPIO.IN,
               GPIO.PUD_DOWN if pull_mode == 'DOWN' else GPIO.PUD_UP)


def write_output(port, value):
    """Write a value to a GPIO."""
    import CHIP_IO.GPIO as GPIO
    GPIO.output(port, value)


def read_input(port):
    """Read a value from a GPIO."""
    import CHIP_IO.GPIO as GPIO
    return GPIO.input(port)


def edge_detect(port, event_callback, bounce):
    """Add detection for RISING and FALLING events."""
    import CHIP_IO.GPIO as GPIO
    GPIO.add_event_detect(
        port,
        GPIO.BOTH,
        event_callback,
        bouncetime=bounce)