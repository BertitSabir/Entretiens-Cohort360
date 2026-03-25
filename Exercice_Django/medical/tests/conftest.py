import pytest

from medical.models import Medication, Patient, Prescription


@pytest.fixture
def patient():
    return Patient(last_name="Dupont", first_name="Marie", birth_date="1985-06-15")


@pytest.fixture
def medication():
    return Medication(
        code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
    )


@pytest.fixture
def prescription(patient, medication):
    return Prescription(
        patient=patient,
        medication=medication,
        start_date="2026-01-01",
        end_date="2026-01-10",
        comment="Aucune allergie connue",
    )


@pytest.fixture
def patient_db(db):
    return Patient.objects.create(
        last_name="Dupont", first_name="Marie", birth_date="1985-06-15"
    )


@pytest.fixture
def medication_db(db):
    return Medication.objects.create(
        code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
    )


@pytest.fixture
def prescription_db(patient_db, medication_db):
    return Prescription.objects.create(
        patient=patient_db,
        medication=medication_db,
        start_date="2026-01-01",
        end_date="2026-01-10",
    )


@pytest.fixture
def prescription_data(patient_db, medication_db):
    return {
        "patient": patient_db.pk,
        "medication": medication_db.pk,
        "start_date": "2026-01-01",
        "end_date": "2026-01-10",
        "status": Prescription.STATUS_VALIDE,
    }
