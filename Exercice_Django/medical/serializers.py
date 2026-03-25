from rest_framework import serializers

from .models import Medication, Patient, Prescription


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "last_name", "first_name", "birth_date"]


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "code", "label", "status"]


class PrescriptionSerializer(serializers.ModelSerializer):
    """Serializer pour la création et la mise à jour d'une prescription."""

    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient",
            "medication",
            "status",
            "start_date",
            "end_date",
            "comment",
        ]

    def validate(self, attrs):
        """Valide que la date de fin est postérieure ou égale à la date de début."""
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError(
                {
                    "end_date": "La date de fin doit être postérieure ou égale "
                    "à la date de début."
                }
            )
        return attrs


class PrescriptionReadSerializer(serializers.ModelSerializer):
    """Serializer pour la lecture d'une prescription avec les détails imbriqués."""

    patient = PatientSerializer(read_only=True)
    medication = MedicationSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient",
            "medication",
            "status",
            "start_date",
            "end_date",
            "comment",
            "created_at",
        ]
