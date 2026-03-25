import pytest
from django.db.models import ProtectedError

from medical.models import Prescription


def test_prescription_str(prescription):
    # Act
    result = str(prescription)

    # Assert
    assert "Dupont" in result
    assert "PARA500" in result


def test_prescription_default_status(prescription):
    # Assert
    assert prescription.status == Prescription.STATUS_EN_ATTENTE


@pytest.mark.django_db
def test_create_prescription(patient_db, medication_db):
    # Arrange & Act
    p = Prescription.objects.create(
        patient=patient_db,
        medication=medication_db,
        start_date="2024-01-01",
        end_date="2024-01-10",
        status=Prescription.STATUS_VALIDE,
    )

    # Assert
    assert p.pk is not None
    assert p.status == Prescription.STATUS_VALIDE
    assert p.comment == ""


@pytest.mark.django_db
def test_cannot_delete_patient_with_prescriptions(prescription_db):
    # Act & Assert
    with pytest.raises(ProtectedError):
        prescription_db.patient.delete()


@pytest.mark.django_db
def test_cannot_delete_medication_with_prescriptions(prescription_db):
    # Act & Assert
    with pytest.raises(ProtectedError):
        prescription_db.medication.delete()
