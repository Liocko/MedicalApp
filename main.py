
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI(title="Medical Data Tracker", version="1.0.0")

# Модели данных
class Patient(BaseModel):
    id: str
    name: str
    birth_date: str
    gender: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: str

class MedicalRecord(BaseModel):
    id: str
    patient_id: str
    diagnosis: str
    treatment: str
    notes: Optional[str] = None
    created_at: str

# Хранилище данных (в реальном приложении будет использоваться БД)
patients_db = {}
records_db = {}

# API endpoints для пациентов
@app.post("/patients/", response_model=Patient)
def create_patient(patient: Patient):
    patient.id = str(uuid.uuid4())
    patient.created_at = datetime.now().isoformat()
    patients_db[patient.id] = patient
    return patient

@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: str):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[patient_id]

@app.get("/patients/", response_model=List[Patient])
def list_patients():
    return list(patients_db.values())

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: str, updated_patient: Patient):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    updated_patient.id = patient_id
    updated_patient.created_at = patients_db[patient_id].created_at
    patients_db[patient_id] = updated_patient
    return updated_patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients_db[patient_id]
    return {"message": "Patient deleted"}

# API endpoints для медицинских записей
@app.post("/records/", response_model=MedicalRecord)
def create_record(record: MedicalRecord):
    record.id = str(uuid.uuid4())
    record.created_at = datetime.now().isoformat()
    records_db[record.id] = record
    return record

@app.get("/records/{record_id}", response_model=MedicalRecord)
def get_record(record_id: str):
    if record_id not in records_db:
        raise HTTPException(status_code=404, detail="Record not found")
    return records_db[record_id]

@app.get("/records/patient/{patient_id}", response_model=List[MedicalRecord])
def list_records_by_patient(patient_id: str):
    return [record for record in records_db.values() if record.patient_id == patient_id]

@app.put("/records/{record_id}", response_model=MedicalRecord)
def update_record(record_id: str, updated_record: MedicalRecord):
    if record_id not in records_db:
        raise HTTPException(status_code=404, detail="Record not found")
    updated_record.id = record_id
    updated_record.created_at = records_db[record_id].created_at
    records_db[record_id] = updated_record
    return updated_record

@app.delete("/records/{record_id}")
def delete_record(record_id: str):
    if record_id not in records_db:
        raise HTTPException(status_code=404, detail="Record not found")
    del records_db[record_id]
    return {"message": "Record deleted"}

@app.get("/")
def read_root():
    return {"message": "Welcome to Medical Data Tracker API"}
