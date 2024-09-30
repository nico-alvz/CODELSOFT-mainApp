import os

class Config:
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    BASE_DELAY = int(os.getenv("BASE_DELAY", 1000)) / 1000
    EXTERNAL_SERVICES = {
        "auth": os.getenv("AUTH_SERVICE_URL"),
        "search": os.getenv("SEARCH_SERVICE_URL"),
        "grades": os.getenv("GRADES_SERVICE_URL"),
        "restrictions": os.getenv("RESTRICTIONS_SERVICE_URL")
    }

    JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
