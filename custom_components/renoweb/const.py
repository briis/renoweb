"""Constants in renoweb component."""

ATTR_DATE_LONG = "date_long"
ATTR_DURATION = "duration"
ATTR_DESCRIPTION = "description"
ATTR_LAST_UPDATE = "last_update"

CONF_ADDRESS = "address"
CONF_ADDRESS_ID = "address_id"
CONF_HOUSE_NUMBER = "house_number"
CONF_MUNICIPALITY = "municipality"
CONF_ROAD_NAME = "road_name"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_ATTRIBUTION = "Data delivered by RenoWeb"
DEFAULT_BRAND = "RenoWeb"
DEFAULT_API_VERSION = "Legacy"
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
