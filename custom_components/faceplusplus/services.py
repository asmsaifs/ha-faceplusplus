import asyncio
import logging
import os
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from .camera_helper import get_image_base64_from_camera, get_image_base64_from_file

_LOGGER = logging.getLogger(__name__)


async def register_services(hass: HomeAssistant, min_confidence: int, api):
    async def handle_add_face(call: ServiceCall):
        entity = call.data["camera_entity"]
        user_id = call.data.get("user_id")

        try:
            image_b64 = await get_image_base64_from_camera(hass, entity)
            if not image_b64:
                _LOGGER.error("No image from camera")
                return
            detection = await api.detect_face_from_base64(image_b64)
            if "faces" not in detection or not detection["faces"]:
                _LOGGER.warning("No face found in image")
                return
            face_token = detection["faces"][0]["face_token"]
            await asyncio.sleep(0.5)
            result = await api.add_face_to_faceset(face_token)
            hass.bus.fire("faceplusplus_face_added", result)
            _LOGGER.info(
                "Added face_token %s to FaceSet %s. Result: %s",
                face_token,
                result,
            )
            await asyncio.sleep(0.5)
            result = await api.set_userid(face_token, user_id)
            _LOGGER.info("Set user_id result: %s", result)
            hass.bus.fire("faceplusplus_user_id_added", result)
            await asyncio.sleep(0.5)
        except Exception as e:
            _LOGGER.error("Error processing camera image %s: %s", entity, e)

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
                if not image_b64:
                    _LOGGER.error("No image from camera")
                    return
                detection = await api.detect_face_from_base64(image_b64)
                if "faces" not in detection or not detection["faces"]:
                    _LOGGER.warning("No face found in image")
                    return
                face_token = detection["faces"][0]["face_token"]
                await asyncio.sleep(0.5)
                result = await api.add_face_to_faceset(face_token)
                hass.bus.fire("faceplusplus_face_added", result)
                _LOGGER.info(
                    "Added face_token %s to FaceSet %s. Result: %s",
                    face_token,
                    result,
                )
                await asyncio.sleep(0.5)
                result = await api.set_userid(face_token, user_id)
                _LOGGER.info("Set user_id result: %s", result)
                hass.bus.fire("faceplusplus_user_id_added", result)
                await asyncio.sleep(0.5)
            except Exception as e:
                _LOGGER.error("Error processing file %s: %s", filename, e)

    async def recognize_face(image_b64):
        if not image_b64:
            _LOGGER.error("No image from camera")
            return {"user_id": "Someone", "confidence": 0, "success": False}
        result = await api.search_face(image_b64)
        if "results" not in result:
            hass.states.async_set(
                "sensor.faceplusplus_recognized_person", "Someone", {"confidence": 0.0}
            )
            _LOGGER.warning("No face match found")
            return {"user_id": "Someone", "confidence": 0, "success": False}
        best_match = result["results"][0]
        user_id = best_match.get("user_id", "Someone") or "Someone"
        confidence = best_match.get("confidence", 0)
        if confidence < min_confidence:
            user_id = "Someone"
            confidence = 0
        else:
            user_id = user_id.capitalize()

        hass.states.async_set(
            "sensor.faceplusplus_recognized_person",
            user_id,
            {"confidence": confidence},
        )
        _LOGGER.info("Recognized user: %s with confidence %.2f", user_id, confidence)
        hass.bus.fire("faceplusplus_face_recognized", result)
        return {
            "user_id": user_id,
            "confidence": confidence,
            "success": True,
        }

    async def handle_recognize_face(call: ServiceCall):
        entity = call.data["camera_entity"]
        image_b64 = await get_image_base64_from_camera(hass, entity)

        return await recognize_face(image_b64)

    async def handle_recognize_face_from_file(call: ServiceCall):
        file_path = call.data.get("file_path")
        image_b64 = await get_image_base64_from_file(file_path)

        return await recognize_face(image_b64)

    hass.services.async_register("faceplusplus", "add_faces", handle_add_face)
    hass.services.async_register(
        "faceplusplus", "add_faces_from_files", handle_add_faces_from_files
    )
    hass.services.async_register(
        "faceplusplus",
        "recognize_face",
        handle_recognize_face,
        supports_response=SupportsResponse.OPTIONAL,
    )
    hass.services.async_register(
        "faceplusplus",
        "recognize_face_from_file",
        handle_recognize_face_from_file,
        supports_response=SupportsResponse.OPTIONAL,
    )
