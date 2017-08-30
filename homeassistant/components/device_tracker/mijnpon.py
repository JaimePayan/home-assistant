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
    
    _LOGGER.debug("setup mijnpon device tracker: %s" % discovery_info)

    # name = position.street + ' ' + position.city
    # self.dev_id = self.position.coordinate.get('Id')
    _LOGGER.debug("mijnpon coordinate: %s" % hass.data[DATA_MIJNPON].position.coordinate)
    interval = DEFAULT_SCAN_INTERVAL
    # see(dev_id='car', host_name='Car', gps=(hass.data[DATA_MIJNPON].position.latitude, hass.data[DATA_MIJNPON].position.longitude), icon='mdi:car')

#, location_name: name, 

    def update(now):
        """Update the car on every interval time."""
        # _LOGGER.debug("mijnpon coordinate: %s" % hass.data[DATA_MIJNPON].position.coordinate)
        position = hass.data[DATA_MIJNPON].position
        attrs = {
            #'speed': position.speed,
            'street': position.street,
            'city': position.city
        }
        see(dev_id='car', host_name='Car', gps=(position.latitude, position.longitude), attributes=attrs, icon='mdi:car')
        track_point_in_utc_time(hass, update, util.dt.utcnow() + interval)
        return True

    return update(util.dt.utcnow())
