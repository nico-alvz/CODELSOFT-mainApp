import os
import json

class Config:
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    MAX_RETRIES = config.get("MAX_RETRIES", 3)
    BASE_DELAY = config.get("BASE_DELAY", 1000) / 1000
    EXTERNAL_SERVICES = {
        "auth": os.getenv("AUTH_SERVICE_URL", config["external_services"]["auth"]),
        "search": os.getenv("SEARCH_SERVICE_URL", config["external_services"]["search"]),
        "grades": os.getenv("GRADES_SERVICE_URL", config["external_services"]["grades"]),
        "restrictions": os.getenv("RESTRICTIONS_SERVICE_URL", config["external_services"]["restrictions"])
    }
    
    JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
