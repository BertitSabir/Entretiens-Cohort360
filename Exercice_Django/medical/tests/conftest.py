import pytest
from rest_framework.test import APIClient

from medical.factories import (
    MedicationFactory,
    PatientFactory,
    PrescriptionFactory,
)
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
    return PatientFactory()


@pytest.fixture
def medication_db(db):
    return MedicationFactory()


@pytest.fixture
def prescription_db(db):
    return PrescriptionFactory()


@pytest.fixture
def prescription_data(patient_db, medication_db):
    return {
        "patient": patient_db.pk,
        "medication": medication_db.pk,
        "start_date": "2026-01-01",
        "end_date": "2026-01-10",
        "status": Prescription.STATUS_VALIDE,
    }


@pytest.fixture
def prescriptions(db):
    p1 = PrescriptionFactory(
        status=Prescription.STATUS_VALIDE,
        start_date="2026-01-01",
        end_date="2026-01-31",
    )
    p2 = PrescriptionFactory(
        status=Prescription.STATUS_EN_ATTENTE,
        start_date="2026-03-01",
        end_date="2026-06-30",
    )
    p3 = PrescriptionFactory(
        status=Prescription.STATUS_SUPPR, start_date="2026-06-01", end_date="2026-12-31"
    )
    return [p1, p2, p3]


@pytest.fixture
def api_client():
    return APIClient()
