import pytest
from src.logic import proxy
from src.logic.weather import Weather

@pytest.fixture
def proxy_instance():
    return proxy.Proxy()

def test_get_weather(proxy_instance):
    weather = proxy_instance.get_weather()
    assert weather is not None
    assert isinstance(weather, Weather)
    assert hasattr(weather, 'state')
    assert hasattr(weather, 'transition')
    assert isinstance(weather.transition, dict)
    assert weather.state in weather.transition