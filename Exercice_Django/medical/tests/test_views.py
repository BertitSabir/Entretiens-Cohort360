import pytest
from rest_framework import status

from medical.models import Prescription


@pytest.mark.django_db
def test_list_prescriptions(api_client, prescription_db):
    # Arrange
    url = "/Prescription"

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert isinstance(response.data[0]["patient"], dict)
    assert isinstance(response.data[0]["medication"], dict)


@pytest.mark.django_db
def test_get_existing_prescription(api_client, prescription_db):
    # Arrange
    url = f"/Prescription/{prescription_db.id}"

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == prescription_db.id


@pytest.mark.django_db
def test_get_nonexistent_prescription(api_client):
    # Arrange
    url = "/Prescription/99999"

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_prescription(api_client, prescription_data):
    # Arrange
    url = "/Prescription"

    # Act
    response = api_client.post(url, prescription_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert Prescription.objects.count() == 1


@pytest.mark.django_db
def test_create_prescription_invalid_dates_returns_400(api_client, prescription_data):
    # Arrange
    url = "/Prescription"
    prescription_data["start_date"] = "2024-01-10"
    prescription_data["end_date"] = "2024-01-01"

    # Act
    response = api_client.post(url, prescription_data)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Prescription.objects.count() == 0
    assert "end_date" in response.data


@pytest.mark.django_db
def test_partial_update_prescription(api_client, prescription_db):
    # Arrange
    url = f"/Prescription/{prescription_db.id}"

    # Act
    response = api_client.patch(url, {"status": Prescription.STATUS_VALIDE})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    prescription_db.refresh_from_db()
    assert prescription_db.status == Prescription.STATUS_VALIDE


@pytest.mark.django_db
def test_full_update_prescription(api_client, prescription_db):
    # Arrange
    url = f"/Prescription/{prescription_db.id}"
    data = {
        "patient": prescription_db.patient.id,
        "medication": prescription_db.medication.id,
        "start_date": "2024-02-01",
        "end_date": "2024-02-28",
        "status": Prescription.STATUS_VALIDE,
    }

    # Act
    response = api_client.put(url, data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    prescription_db.refresh_from_db()
    assert prescription_db.end_date.strftime("%Y-%m-%d") == "2024-02-28"
    assert prescription_db.status == Prescription.STATUS_VALIDE


@pytest.mark.django_db
def test_filter_by_patient(api_client, prescriptions):
    # Arrange
    url = "/Prescription"
    patient_id = prescriptions[0].patient.id

    # Act
    response = api_client.get(url, {"patient": patient_id})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert all(p["patient"]["id"] == patient_id for p in response.data)


@pytest.mark.django_db
def test_filter_by_medicament(api_client, prescriptions):
    # Arrange
    url = "/Prescription"
    medication_id = prescriptions[0].medication.id

    # Act
    response = api_client.get(url, {"medicament": medication_id})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert all(p["medication"]["id"] == medication_id for p in response.data)


@pytest.mark.django_db
def test_filter_by_status(api_client, prescriptions):
    # Arrange
    url = "/Prescription"

    # Act
    response = api_client.get(url, {"status": Prescription.STATUS_VALIDE})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert all(p["status"] == Prescription.STATUS_VALIDE for p in response.data)


@pytest.mark.django_db
def test_filter_by_date_debut_apres(api_client, prescriptions):
    # Arrange
    url = "/Prescription"

    # Act
    response = api_client.get(url, {"date_debut__apres": "2026-02-01"})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_by_date_fin_avant(api_client, prescriptions):
    # Arrange
    url = "/Prescription"

    # Act
    response = api_client.get(url, {"date_fin__avant": "2026-06-30"})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_combined(api_client, prescriptions):
    # Arrange
    url = "/Prescription"
    patient_id = prescriptions[0].patient.id

    # Act
    response = api_client.get(
        url, {"patient": patient_id, "status": Prescription.STATUS_VALIDE}
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert all(p["patient"]["id"] == patient_id for p in response.data)
    assert all(p["status"] == Prescription.STATUS_VALIDE for p in response.data)
