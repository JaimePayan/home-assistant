"""
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.mijnpon/
"""
import logging

from custom_components.mijnpon import DATA_MIJNPON
from homeassistant.components.binary_sensor import (
    BinarySensorDevice, PLATFORM_SCHEMA)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['mijnpon']

SENSOR_TYPES = {
    'ignition': ['Ignition', True, 'power', 'mdi:power', 'mdi:power'],
    'locked': ['Locked', False, 'opening', 'mdi:lock', 'mdi:lock-open'],
    'parking_brake': ['Parking brake', False, 'safety', 'mdi:parking', 'mdi:parking']
}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up a Mijnpon binary sensor."""
    if discovery_info is None:
        return

    devs = list()
    mijnPon = hass.data[DATA_MIJNPON]
    for vehicle in mijnPon.vehicles():
        devs.append(MijnPonBinarySensor(vehicle.license_plate, 'ignition', mijnPon, vehicle))
        devs.append(MijnPonBinarySensor(vehicle.license_plate, 'locked', mijnPon, vehicle))
        devs.append(MijnPonBinarySensor(vehicle.license_plate, 'parking_brake', mijnPon, vehicle))

    add_devices(devs, True)


class MijnPonBinarySensor(BinarySensorDevice):
    """A MijnPon sensor."""

    def __init__(self, name, sensor_type, mijnPon, vehicle):
        """Initialize sensors from the car."""
        self._name = name + ' ' + SENSOR_TYPES[sensor_type][0]
        self._type = sensor_type
        self._vehicle = vehicle
        self._mijnPon = mijnPon
        self._state = None
        self._on_state = SENSOR_TYPES[sensor_type][1]
        self._icon_off = SENSOR_TYPES[sensor_type][3]
        self._icon_on = SENSOR_TYPES[sensor_type][4]
        self._device_class = SENSOR_TYPES[sensor_type][2]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._device_class

    @property
    def icon(self):
        """Return the icon of this sensor."""
        if self.is_on:
            return self._icon_on
        else:
            return self._icon_off

    @property
    def is_on(self):
        """Return the state of the entity."""
        return self._state == self._on_state

    def update(self):
        """Retrieve sensor data from the car."""
        if self._type == 'ignition':
            self._state = self._vehicle.measureddata('Power')
            if self._state == True:
                self._mijnPon.cache_ttl = 30
            else:
                self._mijnPon.cache_ttl = 270
        elif self._type == 'locked':
            self._state = self._vehicle.measureddata('VehicleLocked')
        elif self._type == 'parking_brake':
            self._state = self._vehicle.measureddata('ElectronicParkingBrake')
        else:
            self._state = None
            _LOGGER.warning("Could not retrieve state from %s", self.name)
