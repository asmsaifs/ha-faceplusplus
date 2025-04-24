from homeassistant import config_entries
from homeassistant.helpers import aiohttp_client
import voluptuous as vol


from .const import DOMAIN, DEFAULT_FACESET_NAME, API_URL


class FacePPConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            faceset_id = await self._ensure_faceset_exists(
                user_input["api_key"],
                user_input["api_secret"],
            )
            if faceset_id:
                return self.async_create_entry(
                    title="Face++",
                    data=user_input,
                    options={"faceset_id": faceset_id},
                )
            errors["base"] = "faceset_error"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                    vol.Required("api_secret"): str,
                    vol.Optional("min_confidence", default=80): int,
                }
            ),
            errors=errors,
        )

    async def _ensure_faceset_exists(self, api_key, api_secret):
        """Create or retrieve Face++ Faceset."""
        outer_id = f"homeassistant_{self.flow_id}"
        url = f"{API_URL}/faceset/create"
        session = aiohttp_client.async_get_clientsession(self.hass)
        try:
            async with session.post(
                url,
                data={
                    "api_key": api_key,
                    "api_secret": api_secret,
                    "outer_id": outer_id,
                    "display_name": DEFAULT_FACESET_NAME,
                },
            ) as response:
                data = await response.json()
                return data.get("faceset_token")
        except Exception:
            return None
