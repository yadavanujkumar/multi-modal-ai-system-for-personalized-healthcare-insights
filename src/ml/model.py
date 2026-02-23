# src/ml/model.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import json
from typing import List

# Define database connection URL
DATABASE_URL = "postgresql://user:password@host:port/dbname"

# Create a database engine
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10, pool_recycle=1800, poolclass=QueuePool)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Define relationships
    patient_data = relationship("PatientData", backref="user", lazy=True)

# Define the PatientData model
class PatientData(Base):
    __tablename__ = "patient_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    medical_history = Column(JSONB, nullable=False)
    current_medications = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Define relationships
    user = relationship("User", backref="patient_data", lazy=True)

# Define the ModelInput model
class ModelInput(Base):
    __tablename__ = "model_inputs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    input_data = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Define relationships
    user = relationship("User", backref="model_inputs", lazy=True)

# Define the ModelOutput model
class ModelOutput(Base):
    __tablename__ = "model_outputs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    output_data = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Define relationships
    user = relationship("User", backref="model_outputs", lazy=True)

# Create all tables in the engine
Base.metadata.create_all(engine)

# Define a function to create a new user
def create_user(name: str, email: str):
    user = User(name=name, email=email)
    session = Session()
    session.add(user)
    session.commit()
    return user

# Define a function to create new patient data
def create_patient_data(user_id: int, medical_history: dict, current_medications: dict):
    patient_data = PatientData(user_id=user_id, medical_history=medical_history, current_medications=current_medications)
    session = Session()
    session.add(patient_data)
    session.commit()
    return patient_data

# Define a function to create new model input
def create_model_input(user_id: int, input_data: dict):
    model_input = ModelInput(user_id=user_id, input_data=input_data)
    session = Session()
    session.add(model_input)
    session.commit()
    return model_input

# Define a function to create new model output
def create_model_output(user_id: int, output_data: dict):
    model_output = ModelOutput(user_id=user_id, output_data=output_data)
    session = Session()
    session.add(model_output)
    session.commit()
    return model_output

# Define a function to get all users
def get_all_users():
    session = Session()
    users = session.query(User).all()
    return users

# Define a function to get all patient data for a user
def get_all_patient_data(user_id: int):
    session = Session()
    patient_data = session.query(PatientData).filter(PatientData.user_id == user_id).all()
    return patient_data

# Define a function to get all model inputs for a user
def get_all_model_inputs(user_id: int):
    session = Session()
    model_inputs = session.query(ModelInput).filter(ModelInput.user_id == user_id).all()
    return model_inputs

# Define a function to get all model outputs for a user
def get_all_model_outputs(user_id: int):
    session = Session()
    model_outputs = session.query(ModelOutput).filter(ModelOutput.user_id == user_id).all()
    return model_outputs

# Example usage:
if __name__ == "__main__":
    # Create a new user
    user = create_user("John Doe", "john@example.com")
    print(user.id)

    # Create new patient data for the user
    patient_data = create_patient_data(user.id, {"medical_history": "diabetes"}, {"current_medications": "insulin"})
    print(patient_data.id)

    # Create new model input for the user
    model_input = create_model_input(user.id, {"input_data": "example input"})
    print(model_input.id)

    # Create new model output for the user
    model_output = create_model_output(user.id, {"output_data": "example output"})
    print(model_output.id)

    # Get all users
    users = get_all_users()
    for user in users:
        print(user.id, user.name, user.email)

    # Get all patient data for the user
    patient_data = get_all_patient_data(user.id)
    for data in patient_data:
        print(data.id, data.medical_history, data.current_medications)

    # Get all model inputs for the user
    model_inputs = get_all_model_inputs(user.id)
    for input_data in model_inputs:
        print(input_data.id, input_data.input_data)

    # Get all model outputs for the user
    model_outputs = get_all_model_outputs(user.id)
    for output_data in model_outputs:
        print(output_data.id, output_data.output_data)