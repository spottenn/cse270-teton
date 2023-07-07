import requests
import pytest

from requests_mock.mocker import Mocker

@pytest.fixture
def mock_requests_get_correct(mocker):
    response_json = {}
    
    # Patching requests.get to return a mocked response
    mocker.patch.object(requests, 'get', return_value=MockResponse(response_json))

@pytest.fixture
def mock_requests_get_incorrect(mocker):
    response_json = {}
    
    # Patching requests.get to return a mocked response
    mocker.patch.object(requests, 'get', return_value=MockResponse(response_json, status_code= 401))

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def test_endpoint_with_correct_credentials(mock_requests_get_correct):
    # Call the endpoint with the provided credentials
    response = requests.get('http://127.0.0.1:8000/users/?username=admin&password=qwerty')

    # Verify that the response is HTTP code 200
    assert response.status_code == 200, f'Expected status code 200, but got {response.status_code}'

def test_endpoint_with_incorrect_credentials(mock_requests_get_incorrect):
    # Call the endpoint with incorrect credentials
    response = requests.get('http://127.0.0.1:8000/users/?username=admin&password=admin')

    # Verify that the response is HTTP code 401
    assert response.status_code == 401, f'Expected status code 401, but got {response.status_code}'
