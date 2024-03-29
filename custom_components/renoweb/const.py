"""Constants in renoweb component."""

API_KEY_MUNICIPALITIES = "DDDD4A1D-DDD1-4436-DDDD-3F374DD683A1"
API_KEY = "346B43B0-D1F0-4AFC-9EE8-C4AD1BFDC218"

ATTR_DATA_VALID = "data_valid"
ATTR_DESCRIPTION = "description"
ATTR_ICON_COLOR = "icon_color"
ATTR_NEXT_PICKUP_TEXT = "next_pickup"
ATTR_NEXT_PICKUP_DATE = "next_pickup_date"
ATTR_SCHEDULE = "schedule"
ATTR_REFRESH_TIME = "refresh_time"
ATTR_FORMATTED_STATE_DK = "formatted_state_dk"
ATTR_SHORT_STATE_DK = "short_state_dk"
ATTR_STATE_TEXT = "state_text"

CONF_ADDRESS = "address"
CONF_ADDRESS_ID = "address_id"
CONF_HOUSE_NUMBER = "house_number"
CONF_MUNICIPALITY = "municipality"
CONF_MUNICIPALITY_ID = "municipality_id"
CONF_ROAD_NAME = "road_name"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_ZIPCODE = "zipcode"

DEFAULT_ATTRIBUTION = "Data delivered by RenoWeb"
DEFAULT_BRAND = "RenoWeb"
DEFAULT_API_VERSION = "1.3"
DEFAULT_SCAN_INTERVAL = 6
DOMAIN = "renoweb"

INTEGRATION_PLATFORMS = ["sensor", "binary_sensor"]


ICON_LIST = {
    "Restaffald-Madaffald": "mdi:trash-can",
    "Dagrenovation": "mdi:trash-can",
    "Metal-Glas": "mdi:glass-fragile",
    "PAPPI": "mdi:recycle",
    "Farligt affald": "mdi:biohazard",
    "Tekstiler": "mdi:hanger",
    "Jern": "mdi:bucket",
    "Papir": "mdi:file",
    "Pap": "mdi:note",
    "Plast Metal": "mdi:trash-can-outline",
    "Storskrald": "mdi:table-furniture",
    "Haveaffald": "mdi:leaf",
}
