# src/core/service.py

"""
Core business service layer implementing domain workflows and orchestration logic for personalized healthcare insights.
"""

import logging
from typing import Dict, List
from datetime import datetime
import json
from enum import Enum
from dataclasses import dataclass
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

# Importing dependencies
from src.core.config import Config
from src.core.data import DataRepository
from src.core.ml import ModelPipeline
from src.core.utils import Utils

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Defining enums for service status
class ServiceStatus(Enum):
    """Enum for service status"""
    INITIALIZED = 1
    RUNNING = 2
    STOPPED = 3

# Defining dataclass for patient data
@dataclass
class PatientData:
    """Dataclass for patient data"""
    patient_id: int
    medical_history: List[str]
    current_symptoms: List[str]

# Defining the core service class
class CoreService:
    """Core business service layer implementing domain workflows and orchestration logic"""
    
    def __init__(self, config: Config, data_repository: DataRepository, model_pipeline: ModelPipeline):
        """
        Initializes the core service with configuration, data repository, and model pipeline.
        
        Args:
        - config (Config): Configuration object
        - data_repository (DataRepository): Data repository object
        - model_pipeline (ModelPipeline): Model pipeline object
        """
        self.config = config
        self.data_repository = data_repository
        self.model_pipeline = model_pipeline
        self.status = ServiceStatus.INITIALIZED
        self.patient_data: Dict[int, PatientData] = {}
        
    def start(self):
        """
        Starts the core service.
        """
        logger.info("Starting core service")
        self.status = ServiceStatus.RUNNING
        self.load_patient_data()
        
    def stop(self):
        """
        Stops the core service.
        """
        logger.info("Stopping core service")
        self.status = ServiceStatus.STOPPED
        
    def load_patient_data(self):
        """
        Loads patient data from data repository.
        """
        logger.info("Loading patient data")
        patient_data_list = self.data_repository.get_patient_data()
        for patient_data in patient_data_list:
            self.patient_data[patient_data.patient_id] = patient_data
            
    def get_patient_insights(self, patient_id: int) -> Dict[str, str]:
        """
        Gets personalized healthcare insights for a patient.
        
        Args:
        - patient_id (int): Patient ID
        
        Returns:
        - Dict[str, str]: Patient insights
        """
        logger.info(f"Getting patient insights for patient {patient_id}")
        patient_data = self.patient_data.get(patient_id)
        if patient_data:
            insights = self.model_pipeline.predict(patient_data.medical_history, patient_data.current_symptoms)
            return insights
        else:
            logger.error(f"Patient data not found for patient {patient_id}")
            return {}
        
    def update_patient_data(self, patient_id: int, medical_history: List[str], current_symptoms: List[str]):
        """
        Updates patient data.
        
        Args:
        - patient_id (int): Patient ID
        - medical_history (List[str]): Medical history
        - current_symptoms (List[str]): Current symptoms
        """
        logger.info(f"Updating patient data for patient {patient_id}")
        patient_data = PatientData(patient_id, medical_history, current_symptoms)
        self.patient_data[patient_id] = patient_data
        self.data_repository.update_patient_data(patient_data)
        
# Defining a function to create a core service instance
def create_core_service(config: Config, data_repository: DataRepository, model_pipeline: ModelPipeline) -> CoreService:
    """
    Creates a core service instance.
    
    Args:
    - config (Config): Configuration object
    - data_repository (DataRepository): Data repository object
    - model_pipeline (ModelPipeline): Model pipeline object
    
    Returns:
    - CoreService: Core service instance
    """
    return CoreService(config, data_repository, model_pipeline)

# Example usage
if __name__ == "__main__":
    # Creating configuration, data repository, and model pipeline instances
    config = Config()
    data_repository = DataRepository()
    model_pipeline = ModelPipeline()
    
    # Creating a core service instance
    core_service = create_core_service(config, data_repository, model_pipeline)
    
    # Starting the core service
    core_service.start()
    
    # Getting patient insights
    patient_id = 1
    insights = core_service.get_patient_insights(patient_id)
    print(f"Patient insights for patient {patient_id}: {insights}")
    
    # Updating patient data
    medical_history = ["diabetes", "hypertension"]
    current_symptoms = ["fever", "cough"]
    core_service.update_patient_data(patient_id, medical_history, current_symptoms)
    
    # Stopping the core service
    core_service.stop()