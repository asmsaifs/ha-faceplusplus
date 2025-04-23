import base64
from .const import API_URL
import aiohttp


class FacePlusPlusAPI:
    def __init__(self, api_key, api_secret, faceset_id=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.faceset_token = faceset_id
        self.session = aiohttp.ClientSession()

    async def detect_face_from_base64(self, image_bytes):
        url = f"{API_URL}/detect"
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "image_base64": image_bytes,
            "return_attributes": "age,gender,emotion",
        }
        async with self.session.post(url, data=payload) as response:
            return await response.json()

    async def add_face_to_faceset(self, face_token):
        url = f"{API_URL}/faceset/addface"
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "face_tokens": face_token,
            "faceset_token": self.faceset_token,
        }
        async with self.session.post(url, data=payload) as response:
            return await response.json()

    async def search_face(self, image_bytes):
        url = f"{API_URL}/search"
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "image_base64": image_bytes,
            "faceset_token": self.faceset_token,
        }
        async with self.session.post(url, data=payload) as response:
            return await response.json()

    async def set_userid(self, face_token, user_id):
        url = f"{API_URL}/face/setuserid"
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "face_token": face_token,
            "user_id": user_id,
        }
        async with self.session.post(url, data=payload) as response:
            return await response.json()
