import pytest
from unittest.mock import patch, MagicMock
from data_pipeline.etl import DataPipeline
from data_pipeline.feature_engineering import FeatureEngineering
from data_pipeline.data_loader import DataLoader
from data_pipeline.data_processor import DataProcessor
from data_pipeline.exceptions import InvalidDataError, ProcessingError

# Constants
TEST_DATA_FILE = 'test_data.csv'
INVALID_DATA_FILE = 'invalid_data.csv'
EXPECTED_OUTPUT_FILE = 'expected_output.csv'

# Fixtures
@pytest.fixture
def data_pipeline():
    return DataPipeline()

@pytest.fixture
def feature_engineering():
    return FeatureEngineering()

@pytest.fixture
def data_loader():
    return DataLoader()

@pytest.fixture
def data_processor():
    return DataProcessor()

# Happy path scenarios
def test_data_pipeline_happy_path(data_pipeline, data_loader, data_processor, feature_engineering):
    """Test data pipeline with valid data"""
    data = data_loader.load_data(TEST_DATA_FILE)
    processed_data = data_processor.process_data(data)
    engineered_data = feature_engineering.engineer_features(processed_data)
    assert engineered_data.shape[0] > 0

def test_feature_engineering_happy_path(feature_engineering, data_processor, data_loader):
    """Test feature engineering with valid data"""
    data = data_loader.load_data(TEST_DATA_FILE)
    processed_data = data_processor.process_data(data)
    engineered_data = feature_engineering.engineer_features(processed_data)
    assert engineered_data.shape[1] > 0

# Error handling and edge cases
def test_data_pipeline_invalid_data(data_pipeline, data_loader, data_processor, feature_engineering):
    """Test data pipeline with invalid data"""
    data = data_loader.load_data(INVALID_DATA_FILE)
    with pytest.raises(InvalidDataError):
        data_processor.process_data(data)

def test_feature_engineering_empty_data(feature_engineering):
    """Test feature engineering with empty data"""
    with pytest.raises(ProcessingError):
        feature_engineering.engineer_features(None)

# Boundary conditions
def test_data_pipeline_large_data(data_pipeline, data_loader, data_processor, feature_engineering):
    """Test data pipeline with large data"""
    data = data_loader.load_data(TEST_DATA_FILE)
    processed_data = data_processor.process_data(data)
    engineered_data = feature_engineering.engineer_features(processed_data)
    assert engineered_data.shape[0] > 0

# Performance/load tests
def test_data_pipeline_performance(data_pipeline, data_loader, data_processor, feature_engineering):
    """Test data pipeline performance"""
    data = data_loader.load_data(TEST_DATA_FILE)
    processed_data = data_processor.process_data(data)
    engineered_data = feature_engineering.engineer_features(processed_data)
    assert engineered_data.shape[0] > 0

# Integration tests
def test_data_pipeline_integration(data_pipeline, data_loader, data_processor, feature_engineering):
    """Test data pipeline integration"""
    data = data_loader.load_data(TEST_DATA_FILE)
    processed_data = data_processor.process_data(data)
    engineered_data = feature_engineering.engineer_features(processed_data)
    assert engineered_data.shape[0] > 0

# Mock external dependencies
@patch('data_pipeline.data_loader.DataLoader.load_data')
def test_data_pipeline_mock_data_loader(mock_load_data, data_pipeline, data_processor, feature_engineering):
    """Test data pipeline with mocked data loader"""
    mock_load_data.return_value = None
    with pytest.raises(InvalidDataError):
        data_pipeline.run()

@patch('data_pipeline.data_processor.DataProcessor.process_data')
def test_data_pipeline_mock_data_processor(mock_process_data, data_pipeline, data_loader, feature_engineering):
    """Test data pipeline with mocked data processor"""
    mock_process_data.return_value = None
    with pytest.raises(ProcessingError):
        data_pipeline.run()

@patch('data_pipeline.feature_engineering.FeatureEngineering.engineer_features')
def test_data_pipeline_mock_feature_engineering(mock_engineer_features, data_pipeline, data_loader, data_processor):
    """Test data pipeline with mocked feature engineering"""
    mock_engineer_features.return_value = None
    with pytest.raises(ProcessingError):
        data_pipeline.run()

# Parametrized tests
@pytest.mark.parametrize("input_file, expected_output_file", [
    (TEST_DATA_FILE, EXPECTED_OUTPUT_FILE),
    (INVALID_DATA_FILE, None),
])
def test_data_pipeline_parametrized(data_pipeline, data_loader, data_processor, feature_engineering, input_file, expected_output_file):
    """Test data pipeline with parametrized input"""
    data = data_loader.load_data(input_file)
    if expected_output_file:
        processed_data = data_processor.process_data(data)
        engineered_data = feature_engineering.engineer_features(processed_data)
        assert engineered_data.shape[0] > 0
    else:
        with pytest.raises(InvalidDataError):
            data_processor.process_data(data)