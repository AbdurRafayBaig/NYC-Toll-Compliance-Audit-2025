import os

# Directories
DATA_DIR = "data"
OUTPUT_DIR = "output"

# URLs
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
GEOJSON_URL = "https://data.cityofnewyork.us/resource/8meu-9t5y.geojson?$limit=5000"

# Pipeline Settings
YEARS_TO_DOWNLOAD = [2024, 2025]
TAXIS = ["yellow", "green"]

# Congestion Zone Configuration
CONGESTION_ZONE_IDS = [
    12, 13, 43, 45, 48, 50, 68, 79, 87, 88, 90, 100, 107, 113, 114, 116, 120, 125, 127, 128, 137, 
    140, 141, 142, 143, 144, 148, 151, 152, 153, 158, 161, 162, 163, 164, 166, 170, 186, 209, 211, 
    224, 229, 230, 231, 232, 233, 234, 236, 237, 238, 239, 243, 244, 246, 249, 261, 262, 263
]

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
