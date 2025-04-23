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
    faceset_id = entry.options.get("faceset_id")

    hass.data[DOMAIN]["api"] = FacePlusPlusAPI(api_key, api_secret, faceset_id)

    await register_services(hass, hass.data[DOMAIN]["api"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data[DOMAIN]["api"].session.close()
    hass.data.pop(DOMAIN)
    return True


# async def async_setup(hass, config):
#     return True


# async def async_setup_entry(hass, entry):
#     api_key = entry.data["api_key"]
#     api_secret = entry.data["api_secret"]
#     faceset_id = entry.options.get("faceset_id")
#     await async_setup_services(hass, api_key, api_secret, faceset_id)
#     return True


# async def async_setup_services(hass, api_key, api_secret, faceset_id):
#     async def handle_detect_from_camera(call):
#         entity_id = call.data.get("camera_entity")
#         image = await get_camera_image(hass, entity_id)
#         if not image:
#             _LOGGER.error("Failed to get image from camera")
#             return
#         result = detect_face_from_base64(api_key, api_secret, image)
#         if "faces" not in result or not result["faces"]:
#             _LOGGER.warning("No faces detected")
#             return
#         attributes = result["faces"][0]["attributes"]
#         for attr in ["age", "gender", "emotion"]:
#             sensor_id = f"{DOMAIN}_{attr}"
#             hass.states.async_set(
#                 f"sensor.{sensor_id}",
#                 attributes[attr]["value"]
#                 if attr != "emotion"
#                 else max(attributes["emotion"], key=attributes["emotion"].get),
#             )

#     async def handle_add_face(call):
#         entity_id = call.data.get("camera_entity")
#         user_id = call.data.get("user_id")
#         image = await get_camera_image(hass, entity_id)
#         if not image:
#             _LOGGER.error("No image from camera")
#             return
#         detection = detect_face_from_base64(api_key, api_secret, image)
#         if "faces" not in detection or not detection["faces"]:
#             _LOGGER.warning("No face found in image")
#             return
#         face_token = detection["faces"][0]["face_token"]

#         result = add_face_to_faceset(
#             api_key, api_secret, face_token, faceset_token=faceset_id
#         )
#         _LOGGER.info(
#             "Added face_token %s to FaceSet %s. Result: %s",
#             face_token,
#             faceset_id,
#             result,
#         )
#         result = set_userid(api_key, api_secret, face_token, user_id)
#         _LOGGER.info("Set user_id result: %s", result)

#     async def handle_add_faces_from_files(call):
#         folder_path = call.data.get("folder_path")
#         user_id = call.data.get("user_id")

#         for filename in os.listdir(folder_path):
#             if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
#                 continue
#             try:
#                 with open(os.path.join(folder_path, filename), "rb") as f:
#                     image = f.read()
#                 detection = detect_face_from_base64(api_key, api_secret, image)
#                 if "faces" not in detection or not detection["faces"]:
#                     _LOGGER.warning("No face in image: %s", filename)
#                     continue
#                 face_token = detection["faces"][0]["face_token"]
#                 result = add_face_to_faceset(
#                     api_key, api_secret, face_token, faceset_token=faceset_id
#                 )

#                 _LOGGER.info("Added %s to FaceSet: %s", filename, result)
#                 result = set_userid(api_key, api_secret, face_token, user_id)
#                 _LOGGER.info("Set user_id result: %s", result)
#             except Exception as e:
#                 _LOGGER.error("Error processing file %s: %s", filename, e)

#     async def handle_recognize_face(call):
#         entity_id = call.data.get("camera_entity")
#         image = await get_camera_image(hass, entity_id)
#         if not image:
#             _LOGGER.error("No image from camera")
#             return
#         result = search_face(api_key, api_secret, image, faceset_token=faceset_id)
#         if "results" not in result:
#             _LOGGER.warning("No face match found")
#             return
#         best_match = result["results"][0]
#         user_id = best_match.get("user_id", "Unknown")
#         confidence = best_match.get("confidence", 0)
#         hass.states.async_set(
#             "sensor.faceplusplus_recognized_person", user_id, {"confidence": confidence}
#         )
#         _LOGGER.info("Recognized user: %s with confidence %.2f", user_id, confidence)

#     # async def handle_set_userid(call):
#     #     face_token = call.data.get("face_token")
#     #     user_id = call.data.get("user_id")
#     #     result = set_userid(api_key, api_secret, face_token, user_id)
#     #     _LOGGER.info("Set user_id result: %s", result)

#     hass.services.async_register(
#         DOMAIN, "detect_from_camera", handle_detect_from_camera
#     )
#     hass.services.async_register(DOMAIN, "add_face_to_faceset", handle_add_face)
#     hass.services.async_register(
#         DOMAIN, "add_faces_from_files", handle_add_faces_from_files
#     )
#     hass.services.async_register(DOMAIN, "recognize_face", handle_recognize_face)
#     # hass.services.async_register(DOMAIN, "set_userid", handle_set_userid)
#     return True
