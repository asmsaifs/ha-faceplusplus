import base64
import aiofiles
from homeassistant.core import HomeAssistant
from homeassistant.components.camera import async_get_image

from asyncio import Lock

camera_locks = {}


async def get_image_base64_from_camera(hass: HomeAssistant, entity_id: str) -> str:
    """Safely get base64 image from a camera entity."""
    if entity_id not in camera_locks:
        camera_locks[entity_id] = Lock()

    async with camera_locks[entity_id]:
        try:
            image = await async_get_image(hass, entity_id)
            return base64.b64encode(image.content).decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to get image from camera '{entity_id}': {e}")


# async def get_image_base64_from_camera(hass: HomeAssistant, entity_id: str) -> str:
#     """Get base64 image from a Home Assistant camera entity."""
#     try:
#         image = await async_get_image(hass, entity_id)
#         return base64.b64encode(image.content).decode("utf-8")
#     except Exception as e:
#         raise RuntimeError(f"Failed to get image from camera '{entity_id}': {e}")


async def get_image_base64_from_file(path: str) -> str:
    async with aiofiles.open(path, "rb") as f:
        return base64.b64encode(await f.read()).decode("utf-8")
