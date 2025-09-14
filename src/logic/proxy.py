import requests
import json
import src.config.config as config
from .weather import Weather

# Singleton proxy class to manage API requests
class Proxy:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Proxy, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.base_url = config.URL
        self.offline = False
        # Check healthz
        result = requests.get(f"{self.base_url}/healthz")
        if result.status_code != 200 or not (result.json().get("ok")):
            print(f"Error: API healthz. Status: {result.status_code}")
            print(f"Response: changing to offline mode...")
            self.offline = True

    def _load_cache(self, filename: str):
        with open(f"api_cache/{filename}", 'r') as f:
            data = json.load(f)
        return data

    def get_weather(self) -> Weather:
        # Load data
        if not self.offline:
            result = requests.get(f"{self.base_url}/city/weather")
            if result.status_code == 200:
                data = result.json()
                # cache the data
                with open("api_cache/weather.json", 'w') as f:
                    json.dump(data, f)
            if result.status_code != 200:
                data = self._load_cache("weather.json")
        elif self.offline:
            data = self._load_cache("weather.json")
        data = data.get("data", {})
        # Parse data
        initial_condition = data.get("initial").get("condition")
        transition = data.get("transition")
        weather = Weather(initial_state=initial_condition,
                          transition=transition)
        return weather
