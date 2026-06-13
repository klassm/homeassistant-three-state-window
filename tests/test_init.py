"""Tests for the Three State Window integration."""

from homeassistant import config_entries
from homeassistant.const import STATE_OFF, STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.three_state_window.const import (
    DOMAIN,
    STATE_CLOSED,
    STATE_OPEN,
    STATE_TILTED,
)

CONTACT_SENSOR = "binary_sensor.window_contact"
TILT_SENSOR = "binary_sensor.window_tilt"


def _create_entry(hass: HomeAssistant, entry_id: str = "test1") -> MockConfigEntry:
    entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id=entry_id,
        title="Test Window",
        data={
            "name": "Test Window",
            "contact_sensor": CONTACT_SENSOR,
            "tilt_sensor": TILT_SENSOR,
        },
    )
    entry.add_to_hass(hass)
    return entry


async def _setup_sources(hass: HomeAssistant, contact: str, tilt: str) -> None:
    hass.states.async_set(CONTACT_SENSOR, contact)
    hass.states.async_set(TILT_SENSOR, tilt)
    await hass.async_block_till_done()


async def _setup_entry(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_sensor_closed(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_OFF, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("sensor.test_window")
    assert state is not None
    assert state.state == STATE_CLOSED


async def test_sensor_tilted(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_ON, STATE_OFF)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("sensor.test_window")
    assert state is not None
    assert state.state == STATE_TILTED


async def test_sensor_open(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_ON, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("sensor.test_window")
    assert state is not None
    assert state.state == STATE_OPEN


async def test_sensor_unavailable_when_source_missing(hass: HomeAssistant) -> None:
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("sensor.test_window")
    assert state is not None
    assert state.state == STATE_UNAVAILABLE


async def test_sensor_unavailable_when_source_unknown(hass: HomeAssistant) -> None:
    hass.states.async_set(CONTACT_SENSOR, STATE_UNKNOWN)
    hass.states.async_set(TILT_SENSOR, STATE_OFF)
    await hass.async_block_till_done()

    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("sensor.test_window")
    assert state is not None
    assert state.state == STATE_UNAVAILABLE


async def test_sensor_state_change(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_OFF, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("sensor.test_window")
    assert state.state == STATE_CLOSED

    hass.states.async_set(CONTACT_SENSOR, STATE_ON)
    hass.states.async_set(TILT_SENSOR, STATE_OFF)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.test_window").state == STATE_TILTED

    hass.states.async_set(TILT_SENSOR, STATE_ON)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.test_window").state == STATE_OPEN

    hass.states.async_set(CONTACT_SENSOR, STATE_OFF)
    hass.states.async_set(TILT_SENSOR, STATE_ON)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.test_window").state == STATE_CLOSED


async def test_binary_sensor_off_when_closed(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_OFF, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("binary_sensor.test_window_open")
    assert state is not None
    assert state.state == STATE_OFF


async def test_binary_sensor_on_when_tilted(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_ON, STATE_OFF)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("binary_sensor.test_window_open")
    assert state.state == STATE_ON


async def test_binary_sensor_on_when_open(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_ON, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("binary_sensor.test_window_open")
    assert state.state == STATE_ON


async def test_binary_sensor_unavailable_when_source_missing(hass: HomeAssistant) -> None:
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    state = hass.states.get("binary_sensor.test_window_open")
    assert state is not None
    assert state.state == STATE_UNAVAILABLE


async def test_binary_sensor_state_change(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_OFF, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    assert hass.states.get("binary_sensor.test_window_open").state == STATE_OFF

    hass.states.async_set(CONTACT_SENSOR, STATE_ON)
    hass.states.async_set(TILT_SENSOR, STATE_OFF)
    await hass.async_block_till_done()
    assert hass.states.get("binary_sensor.test_window_open").state == STATE_ON

    hass.states.async_set(CONTACT_SENSOR, STATE_OFF)
    hass.states.async_set(TILT_SENSOR, STATE_ON)
    await hass.async_block_till_done()
    assert hass.states.get("binary_sensor.test_window_open").state == STATE_OFF


async def test_binary_sensor_ignores_tilt_state(hass: HomeAssistant) -> None:
    """Window is closed when contact is OFF regardless of tilt sensor state.

    The tilt sensor is OFF when the window is tilted (contact closed on the
    tilt sensor). When the window is fully closed, the tilt sensor is ON
    (its contact is open). The binary sensor must only look at the contact
    sensor to determine if the window is not-closed.
    """
    await _setup_sources(hass, STATE_OFF, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    assert hass.states.get("binary_sensor.test_window_open").state == STATE_OFF


async def test_config_flow(hass: HomeAssistant) -> None:
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "name": "Living Room Window",
            "contact_sensor": "binary_sensor.living_contact",
            "tilt_sensor": "binary_sensor.living_tilt",
        },
    )
    assert result["type"] == "create_entry"
    assert result["title"] == "Living Room Window"
    assert result["data"] == {
        "name": "Living Room Window",
        "contact_sensor": "binary_sensor.living_contact",
        "tilt_sensor": "binary_sensor.living_tilt",
    }


async def test_config_flow_duplicate_abort(hass: HomeAssistant) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="existing",
        title="Existing Window",
        data={
            "name": "Existing Window",
            "contact_sensor": "binary_sensor.dup_contact",
            "tilt_sensor": "binary_sensor.dup_tilt",
        },
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "name": "Duplicate Window",
            "contact_sensor": "binary_sensor.dup_contact",
            "tilt_sensor": "binary_sensor.dup_tilt",
        },
    )
    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"


async def test_unload_entry(hass: HomeAssistant) -> None:
    await _setup_sources(hass, STATE_OFF, STATE_ON)
    entry = _create_entry(hass)
    await _setup_entry(hass, entry)

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.test_window").state == STATE_UNAVAILABLE
    assert hass.states.get("binary_sensor.test_window_open").state == STATE_UNAVAILABLE


async def test_multiple_instances(hass: HomeAssistant) -> None:
    """Verify two windows can coexist with different names and entity IDs."""
    contact2 = "binary_sensor.window2_contact"
    tilt2 = "binary_sensor.window2_tilt"

    await _setup_sources(hass, STATE_ON, STATE_OFF)
    hass.states.async_set(contact2, STATE_OFF)
    hass.states.async_set(tilt2, STATE_ON)
    await hass.async_block_till_done()

    entry1 = _create_entry(hass, "test1")
    await _setup_entry(hass, entry1)

    entry2 = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test2",
        title="Bedroom Window",
        data={
            "name": "Bedroom Window",
            "contact_sensor": contact2,
            "tilt_sensor": tilt2,
        },
    )
    entry2.add_to_hass(hass)
    await _setup_entry(hass, entry2)

    assert hass.states.get("sensor.test_window").state == STATE_TILTED
    assert hass.states.get("sensor.bedroom_window").state == STATE_CLOSED
    assert hass.states.get("binary_sensor.test_window_open").state == STATE_ON
    assert hass.states.get("binary_sensor.bedroom_window_open").state == STATE_OFF
