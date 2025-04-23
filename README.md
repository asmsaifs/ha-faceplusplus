# 🧠 Face++ Custom Integration for Home Assistant

This Home Assistant custom integration lets you connect to [Face++ (faceplusplus.com)](https://www.faceplusplus.com/) for powerful face recognition features. Add faces to a FaceSet using your camera or local images, and identify people in real time from your Home Assistant camera feeds.

---

## ✨ Features

- ✅ **Add faces** to a FaceSet from:
  - Camera snapshots
  - Uploaded image files
- ✅ **Recognize faces** using the Face++ API
- ✅ **UI-based configuration**

---

## Install

### Installation via HACS

Have [HACS](https://hacs.xyz/) installed, this will allow you to update easily.

* Adding Face++ to HACS can be using this button:

[![image](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=asmsaifs&repository=faceplusplus&category=integration)

> [!NOTE]
> If the button above doesn't work, add `https://github.com/asmsaifs/ha-faceplusplus` as a custom repository of type Integration in HACS.

* Click Install on the `Proxmox VE` integration.
* Restart the Home Assistant.

<details><summary>Manual installation</summary>
 
* Copy `faceplusplus`  folder from [latest release](https://github.com/asmsaifs/ha-faceplusplus/releases/latest) to [`custom_components` folder](https://developers.home-assistant.io/docs/creating_integration_file_structure/#where-home-assistant-looks-for-integrations) in your config directory.
* Restart the Home Assistant.
</details>


## 📁 Configuration

1. Clone this repository into your `custom_components` folder:
   ```bash
   git clone https://github.com/yourusername/ha-faceplusplus.git custom_components/faceplusplus

> [⚙️ Configuration](https://my.home-assistant.io/redirect/config) > Devices and Services > [🧩 Integrations](https://my.home-assistant.io/redirect/integrations) > [➕ Add Integration](https://my.home-assistant.io/redirect/config_flow_start?domain=faceplusplus) > 🔍 Search `Face++`

Or click: [![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=faceplusplus)


## Services

### `faceplusplus.add_faces`

Add faces from camera.

**Example service data:**
```yaml
camera_entity: camera.living_room
user_id: Karim
```

---

### `faceplusplus.add_faces_from_files`

Add faces from files in given folder path.

**Example service data:**
```yaml
folder_path: /config/www/faces
user_id: Karim
```

---

### `faceplusplus.recognize_face`

Recognizes a face from a camera snapshot.

**Example service data:**
```yaml
camera_entity: camera.front_door
```

---

### `faceplusplus.recognize_face_from_file`

Recognizes a face from a image file.

**Example service data:**
```yaml
file_path: /config/www/faces/karim-1.jpg
```

## Known Limitations

- Only one face is processed per frame.
- Camera snapshots must be accessible through Home Assistant.

## License

[MIT License](LICENSE)

## Contributing

Pull requests and feature suggestions are welcome!

---

**Note**: This is a community integration and is not officially supported by Face++ or Home Assistant.
