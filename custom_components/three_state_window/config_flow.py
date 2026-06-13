"""Config flow for Three State Window."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("contact_sensor"): selector.EntitySelector(selector.EntitySelectorConfig(domain="binary_sensor")),
        vol.Required("tilt_sensor"): selector.EntitySelector(selector.EntitySelectorConfig(domain="binary_sensor")),
    }
)


class ThreeStateWindowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self._async_abort_entries_match(
                {
                    "contact_sensor": user_input["contact_sensor"],
                    "tilt_sensor": user_input["tilt_sensor"],
                }
            )
            return self.async_create_entry(title=user_input["name"], data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
