"""Combined binary sensor (on when open or tilted)."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    contact = entry.data["contact_sensor"]
    tilt = entry.data["tilt_sensor"]
    async_add_entities([WindowBinarySensor(entry, contact, tilt)])


class WindowBinarySensor(BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.WINDOW
    _attr_translation_key = "window_open"

    def __init__(self, entry: ConfigEntry, contact_sensor: str, tilt_sensor: str):
        self._contact_sensor = contact_sensor
        self._tilt_sensor = tilt_sensor
        self._attr_unique_id = f"{entry.entry_id}_binary"
        self._attr_name = f"{entry.data['name']} Open"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
        )

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._contact_sensor, self._tilt_sensor],
                self._state_changed,
            )
        )
        self._update_state()

    @callback
    def _state_changed(self, event):
        self._update_state()
        self.async_write_ha_state()

    @callback
    def _update_state(self):
        tilt_state = self.hass.states.get(self._tilt_sensor)
        contact_state = self.hass.states.get(self._contact_sensor)
        if tilt_state is None or contact_state is None:
            self._attr_available = False
            return
        if tilt_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE) or contact_state.state in (
            STATE_UNKNOWN,
            STATE_UNAVAILABLE,
        ):
            self._attr_available = False
            return
        self._attr_available = True
        self._attr_is_on = contact_state.state == STATE_ON
