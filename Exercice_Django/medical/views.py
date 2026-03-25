from rest_framework import viewsets

from .filters import MedicationFilter, PatientFilter, PrescriptionFilter
from .models import Medication, Patient, Prescription
from .serializers import (
    MedicationSerializer,
    PatientSerializer,
    PrescriptionReadSerializer,
    PrescriptionSerializer,
)


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture seule des patients avec filtrage via query params."""

    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filterset_class = PatientFilter


class MedicationViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture seule des médicaments avec filtrage via query params."""

    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    filterset_class = MedicationFilter


class PrescriptionViewSet(viewsets.ModelViewSet):
    """Création, lecture et mise à jour des prescriptions."""

    queryset = Prescription.objects.select_related("patient", "medication").order_by(
        "-created_at"
    )
    filterset_class = PrescriptionFilter

    def get_serializer_class(self):
        # Read: nested objects (patient, medication) to avoid exposing raw IDs
        # Write: FK IDs for validation and creation
        if self.request.method == "GET":
            return PrescriptionReadSerializer
        return PrescriptionSerializer
