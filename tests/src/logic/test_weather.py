import pytest
import json
from src.logic.weather import Weather

@pytest.fixture
def weather():
    with open("tests/data/weather.json", 'r') as f:
        data = json.load(f)
        data = data["data"]
        transition = data["transition"]
        initial_state = data["initial"]["condition"]
    return Weather(initial_state=initial_state, transition=transition)

def test_next_state(weather):
    current_state = weather.state
    next_state = weather.next_state()
    print(f"Current state: {current_state}, Next state: {next_state}")
    assert next_state in weather.transition[current_state]