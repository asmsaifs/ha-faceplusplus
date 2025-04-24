from .const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .faceplusplus import FacePlusPlusAPI
from .services import register_services


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    api_key = entry.data["api_key"]
    api_secret = entry.data["api_secret"]
    min_confidence = entry.data.get("min_confidence", 80)
    faceset_id = entry.options.get("faceset_id")

    hass.data[DOMAIN]["api"] = FacePlusPlusAPI(api_key, api_secret, faceset_id)

    await register_services(hass, min_confidence, hass.data[DOMAIN]["api"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data[DOMAIN]["api"].session.close()
    hass.data.pop(DOMAIN)
    return True
