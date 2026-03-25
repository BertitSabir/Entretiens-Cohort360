from medical.models import Prescription
from medical.serializers import PrescriptionReadSerializer, PrescriptionSerializer


def test_serializer_invalid_patient(medication_db):
    # Arrange
    data = {
        "patient": 99999,
        "medication": medication_db.pk,
        "start_date": "2026-01-01",
        "end_date": "2026-01-10",
        "status": Prescription.STATUS_VALIDE,
    }

    # Act
    serializer = PrescriptionSerializer(data=data)

    # Assert
    assert not serializer.is_valid()
    assert "patient" in serializer.errors


def test_serializer_invalid_medication(patient_db):
    # Arrange
    data = {
        "patient": patient_db.pk,
        "medication": 99999,
        "start_date": "2026-01-01",
        "end_date": "2026-01-10",
        "status": Prescription.STATUS_VALIDE,
    }

    # Act
    serializer = PrescriptionSerializer(data=data)

    # Assert
    assert not serializer.is_valid()
    assert "medication" in serializer.errors


def test_serializer_valid(prescription_data):
    # Act
    serializer = PrescriptionSerializer(data=prescription_data)

    # Assert
    assert serializer.is_valid(), serializer.errors


def test_serializer_end_date_before_start_date(prescription_data):
    # Arrange
    prescription_data["start_date"] = "2026-01-10"
    prescription_data["end_date"] = "2026-01-01"

    # Act
    serializer = PrescriptionSerializer(data=prescription_data)

    # Assert
    assert not serializer.is_valid()
    assert "end_date" in serializer.errors


def test_serializer_end_date_equals_start_date(prescription_data):
    # Arrange
    prescription_data["start_date"] = "2026-01-01"
    prescription_data["end_date"] = "2026-01-01"

    # Act
    serializer = PrescriptionSerializer(data=prescription_data)

    # Assert
    assert serializer.is_valid(), serializer.errors


def test_serializer_missing_required_fields():
    # Act
    serializer = PrescriptionSerializer(data={})

    # Assert
    assert not serializer.is_valid()
    assert "patient" in serializer.errors
    assert "medication" in serializer.errors
    assert "start_date" in serializer.errors
    assert "end_date" in serializer.errors


def test_read_serializer(prescription_db):
    # Act
    data = PrescriptionReadSerializer(prescription_db).data

    # Assert
    assert set(data.keys()) == {
        "id",
        "patient",
        "medication",
        "status",
        "start_date",
        "end_date",
        "comment",
        "created_at",
    }
    assert isinstance(data["patient"], dict)
    assert isinstance(data["medication"], dict)
    assert data["patient"]["id"] == prescription_db.patient.id
    assert data["medication"]["id"] == prescription_db.medication.id
