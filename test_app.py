import pytest
import requests
from app import fetch_url_data


@pytest.fixture
def default_urls():
    return ["https://takehome.io/instagram", "https://takehome.io/facebook", "https://takehome.io/twitter"]


def test_fetch_url_data(default_urls):
    for url in default_urls:
        response = requests.get(url)

        assert response.status_code == 200
