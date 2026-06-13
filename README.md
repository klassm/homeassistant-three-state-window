# Three State Window

A Home Assistant custom integration that combines two binary sensors (contact + tilt) into a single 3-state window sensor.

## Why?

Windows with separate contact and tilt sensors show up as two independent binary sensors in Home Assistant. This integration merges them into one entity with three states: **Open**, **Tilted**, and **Closed** — with proper translations in the frontend.

Template sensors with `device_class: enum` have no way to provide translation strings. Integrations can provide translations via `strings.json` + `translation_key`. This integration makes that pattern reusable for any window with separate contact + tilt binary sensors.

## States

| State | Condition |
|-------|-----------|
| Open | contact sensor ON, tilt sensor ON |
| Tilted | contact sensor ON, tilt sensor OFF |
| Closed | contact sensor OFF |

## Entities

- **Sensor** — 3-state enum sensor (`open` / `tilted` / `closed`) with translated state labels and icons
- **Binary Sensor** — combined window sensor that is ON when the window is open or tilted

Both entities share a single device in the Home Assistant UI.

## Installation

### HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=klassm&repository=homeassistant-three-state-window&category=integration)

### Manual

Copy the `custom_components/three_state_window/` directory to your Home Assistant `custom_components/` directory and restart.

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for **Three State Window**
3. Enter a name and select your contact and tilt binary sensors
4. The **contact sensor** should be the binary sensor that is ON when the window is open (either tilted or fully open)
5. The **tilt sensor** should be the binary sensor that is OFF (closed) when the window is in the tilted position

## Languages

- English
- German (Deutsch)
