"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.mijnpon/
"""
import logging

from custom_components.mijnpon import DATA_MIJNPON
from homeassistant.components.device_tracker import (
    PLATFORM_SCHEMA, DEFAULT_SCAN_INTERVAL)
from homeassistant.helpers.event import track_point_in_utc_time
from homeassistant import util

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mijnpon']

def setup_scanner(hass, config, see, discovery_info=None):
    """Set up a Mijnpon tracker."""
    if discovery_info is None:
        return
    
    interval = DEFAULT_SCAN_INTERVAL

    def update(now):
        """Update the car on every interval time."""
        position = hass.data[DATA_MIJNPON].position
        attrs = {
            'street': position.street,
            'city': position.city,
            'speed': position.speed
        }
        see(dev_id='car', host_name='Car', gps=(position.latitude, position.longitude), attributes=attrs, icon='mdi:car')
        track_point_in_utc_time(hass, update, util.dt.utcnow() + interval)
        return True

    return update(util.dt.utcnow())
