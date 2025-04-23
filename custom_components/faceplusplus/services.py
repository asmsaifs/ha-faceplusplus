import asyncio
import logging
import os
from homeassistant.core import HomeAssistant, ServiceCall
from .camera_helper import get_image_base64_from_camera, get_image_base64_from_file

_LOGGER = logging.getLogger(__name__)


async def register_services(hass: HomeAssistant, api):
    async def handle_add_face(call: ServiceCall):
        entity = call.data["entity_id"]
        user_id = call.data.get("user_id")

        image_b64 = await get_image_base64_from_camera(hass, entity)
        if not image_b64:
            _LOGGER.error("No image from camera")
            return
        detection = await api.detect_face_from_base64(image_b64)
        if "faces" not in detection or not detection["faces"]:
            _LOGGER.warning("No face found in image")
            return
        face_token = detection["faces"][0]["face_token"]

        result = await api.add_face_to_faceset(face_token)
        hass.bus.fire("faceplusplus_face_added", result)
        _LOGGER.info(
            "Added face_token %s to FaceSet %s. Result: %s",
            face_token,
            result,
        )
        result = await api.set_userid(face_token, user_id)
        _LOGGER.info("Set user_id result: %s", result)
        hass.bus.fire("faceplusplus_user_id_added", result)

    async def handle_add_faces_from_files(call):
        folder_path = call.data.get("folder_path")
        user_id = call.data.get("user_id")

        filenames = await asyncio.to_thread(os.listdir, folder_path)

        for filename in filenames:
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            try:
                image_b64 = await get_image_base64_from_file(
                    os.path.join(folder_path, filename)
                )
                detection = await api.detect_face_from_base64(image_b64)
                if "faces" not in detection or not detection["faces"]:
                    _LOGGER.warning("No face found in image")
                    return
                face_token = detection["faces"][0]["face_token"]

                result = await api.add_face_to_faceset(face_token)
                hass.bus.fire("faceplusplus_face_added", result)
                _LOGGER.info(
                    "Added face_token %s to FaceSet %s. Result: %s",
                    face_token,
                    result,
                )
                result = await api.set_userid(face_token, user_id)
                _LOGGER.info("Set user_id result: %s", result)
                hass.bus.fire("faceplusplus_user_id_added", result)
            except Exception as e:
                _LOGGER.error("Error processing file %s: %s", filename, e)

    async def handle_recognize_face(call: ServiceCall):
        entity = call.data["entity_id"]
        image_b64 = await get_image_base64_from_camera(hass, entity)

        if not image_b64:
            _LOGGER.error("No image from camera")
            return
        result = await api.search_face(image_b64)
        if "results" not in result:
            _LOGGER.warning("No face match found")
            return
        best_match = result["results"][0]
        user_id = best_match.get("user_id", "Unknown")
        confidence = best_match.get("confidence", 0)
        hass.states.async_set(
            "sensor.faceplusplus_recognized_person", user_id, {"confidence": confidence}
        )
        _LOGGER.info("Recognized user: %s with confidence %.2f", user_id, confidence)
        hass.bus.fire("faceplusplus_face_recognized", result)

    async def handle_recognize_face_from_file(call: ServiceCall):
        file_path = call.data.get("file_path")
        image_b64 = await get_image_base64_from_file(file_path)

        if not image_b64:
            _LOGGER.error("No image from camera")
            return
        result = await api.search_face(image_b64)
        if "results" not in result:
            _LOGGER.warning("No face match found")
            return
        best_match = result["results"][0]
        user_id = best_match.get("user_id", "Unknown") or "Unknown"
        confidence = best_match.get("confidence", 0)
        hass.states.async_set(
            "sensor.faceplusplus_recognized_person", user_id, {"confidence": confidence}
        )
        _LOGGER.info("Recognized user: %s with confidence %.2f", user_id, confidence)
        hass.bus.fire("faceplusplus_face_recognized", result)

    hass.services.async_register("faceplusplus", "add_faces", handle_add_face)
    hass.services.async_register(
        "faceplusplus", "add_faces_from_files", handle_add_faces_from_files
    )
    hass.services.async_register(
        "faceplusplus", "recognize_face", handle_recognize_face
    )
    hass.services.async_register(
        "faceplusplus", "recognize_face_from_file", handle_recognize_face_from_file
    )
