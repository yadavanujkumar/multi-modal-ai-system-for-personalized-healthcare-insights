import pytest
from typing import Dict, List
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app
from inference import InferenceAPI
from constants import TEST_DATA_DIR, MODEL_NAME

# Fixtures
@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)

@pytest.fixture
def inference_api():
    """Create an instance of the InferenceAPI class"""
    return InferenceAPI()

@pytest.fixture
def test_data():
    """Load test data from file"""
    import json
    with open(f"{TEST_DATA_DIR}/test_data.json", "r") as f:
        return json.load(f)

# Happy path scenarios
def test_inference_api_happy_path(client: TestClient, inference_api: InferenceAPI, test_data: Dict):
    """Test the inference API with valid input data"""
    response = client.post("/inference", json=test_data)
    assert response.status_code == 200
    assert response.json()["prediction"] is not None

def test_inference_api_multiple_inputs(client: TestClient, inference_api: InferenceAPI, test_data: Dict):
    """Test the inference API with multiple input scenarios"""
    input_scenarios = [
        {"input1": "value1", "input2": "value2"},
        {"input1": "value3", "input2": "value4"},
    ]
    for input_scenario in input_scenarios:
        response = client.post("/inference", json=input_scenario)
        assert response.status_code == 200
        assert response.json()["prediction"] is not None

# Error handling and edge cases
def test_inference_api_invalid_input(client: TestClient, inference_api: InferenceAPI):
    """Test the inference API with invalid input data"""
    response = client.post("/inference", json={"invalid": "input"})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

def test_inference_api_missing_input(client: TestClient, inference_api: InferenceAPI):
    """Test the inference API with missing input data"""
    response = client.post("/inference", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

# Boundary conditions
def test_inference_api_large_input(client: TestClient, inference_api: InferenceAPI):
    """Test the inference API with large input data"""
    large_input = {"input1": "a" * 1000, "input2": "b" * 1000}
    response = client.post("/inference", json=large_input)
    assert response.status_code == 200
    assert response.json()["prediction"] is not None

def test_inference_api_empty_input(client: TestClient, inference_api: InferenceAPI):
    """Test the inference API with empty input data"""
    response = client.post("/inference", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

# Performance/load tests
def test_inference_api_performance(client: TestClient, inference_api: InferenceAPI):
    """Test the inference API performance under heavy load"""
    import time
    start_time = time.time()
    for _ in range(100):
        response = client.post("/inference", json={"input1": "value1", "input2": "value2"})
        assert response.status_code == 200
        assert response.json()["prediction"] is not None
    end_time = time.time()
    assert end_time - start_time < 10  # 10 seconds

# Integration tests
def test_inference_api_integration(client: TestClient, inference_api: InferenceAPI):
    """Test the inference API integration with the model"""
    response = client.post("/inference", json={"input1": "value1", "input2": "value2"})
    assert response.status_code == 200
    assert response.json()["prediction"] is not None
    assert response.json()["model"] == MODEL_NAME

# Parametrized tests
@pytest.mark.parametrize("input_scenario", [
    {"input1": "value1", "input2": "value2"},
    {"input1": "value3", "input2": "value4"},
])
def test_inference_api_parametrized(client: TestClient, inference_api: InferenceAPI, input_scenario: Dict):
    """Test the inference API with parametrized input scenarios"""
    response = client.post("/inference", json=input_scenario)
    assert response.status_code == 200
    assert response.json()["prediction"] is not None

# Mocking external dependencies
def test_inference_api_mocked(client: TestClient, inference_api: InferenceAPI, monkeypatch):
    """Test the inference API with mocked external dependencies"""
    mock_model = Mock()
    monkeypatch.setattr(inference_api, "model", mock_model)
    response = client.post("/inference", json={"input1": "value1", "input2": "value2"})
    assert response.status_code == 200
    assert response.json()["prediction"] is not None
    mock_model.predict.assert_called_once()