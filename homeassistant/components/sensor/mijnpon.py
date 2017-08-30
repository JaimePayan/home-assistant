"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.mijnpon/
"""
import logging

from custom_components.mijnpon import DATA_MIJNPON
from homeassistant.const import (LENGTH_KILOMETERS, VOLUME_LITERS)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mijnpon']

SENSOR_TYPES = {
    'mileage': ['Mileage', LENGTH_KILOMETERS],
    'mileage_left': ['Mileage Left', LENGTH_KILOMETERS],
    'fuel_left': ['Fuel Left', VOLUME_LITERS]
}


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up a Mijnpon sensor."""
    if discovery_info is None:
        return

    devs = list()
    for vehicle in hass.data[DATA_MIJNPON].vehicles():
        devs.append(MijnPonSensor(vehicle.license_plate, 'mileage', vehicle))
        devs.append(MijnPonSensor(vehicle.license_plate, 'mileage_left', vehicle))
        devs.append(MijnPonSensor(vehicle.license_plate, 'fuel_left', vehicle))

    add_devices(devs, True)


class MijnPonSensor(Entity):
    """A MijnPon sensor."""

    def __init__(self, name, sensor_type, vehicle):
        """Initialize sensors from the car."""
        self._name = name + ' ' + SENSOR_TYPES[sensor_type][0]
        self._type = sensor_type
        self._vehicle = vehicle
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]

    @property
    def name(self):
        """Return the name of the car."""
        return self._name

    @property
    def state(self):
        """Return the current state."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """Retrieve sensor data from the car."""
        if self._type == 'mileage':
            self._state = self._vehicle.mileage
            _LOGGER.debug("State of %s is: %", (self.name, self._vehicle.mileage))
        elif self._type == 'mileage_left':
            self._state = self._vehicle.mileage_left
        elif self._type == 'fuel_left':
            self._state = self._vehicle.fuel_left
        else:
            self._state = None
            _LOGGER.warning("Could not retrieve state from %s", self.name)
