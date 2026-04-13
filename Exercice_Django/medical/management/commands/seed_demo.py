"""
A management command to seed the database with demo data.

This script creates random records of Patients, Medications, and Prescriptions.
The number of records generated for each model is configurable through command-
line arguments.

Classes:
    Command: A Django management command to seed the database.
"""

import random

from django.core.management.base import BaseCommand
from django.db import connection

from medical.factories import MedicationFactory, PatientFactory, PrescriptionFactory
from medical.models import Medication, Patient, Prescription


def generate_patients(n: int) -> list[Patient]:
    """Generate a list of n random Patient objects using factory boy factories."""
    return PatientFactory.build_batch(n)


def generate_medications(n: int) -> list[Medication]:
    """Generate a list of n random Medication objects using factory boy factories."""
    return MedicationFactory.build_batch(n)


def generate_prescriptions(
    n: int, patients: list[Patient], medications: list[Medication]
):
    """Generate a list of n random Prescription objects using factory boy
    factories and the given patients and medications.
    """
    return PrescriptionFactory.build_batch(
        n, patient=random.choice(patients), medication=random.choice(medications)
    )


def clean_database():
    """Clear existing data from the database.
    This function deletes all records from the Prescription, Patient, and Medication
    and resets the Primary key sequence indices.
    """

    # Clear tables data
    Prescription.objects.all().delete()
    Patient.objects.all().delete()
    Medication.objects.all().delete()

    # Reset auto-increment counters (SQLite only)
    with connection.cursor() as cursor:
        for table in ["medical_prescription", "medical_patient", "medical_medication"]:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")


class Command(BaseCommand):
    help = "Seed the database with demo Patients, Medications, and Prescriptions"

    def add_arguments(self, parser):
        parser.add_argument("--patients", type=int, default=10)
        parser.add_argument("--medications", type=int, default=5)
        parser.add_argument("--prescriptions", type=int, default=30)
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data",
            default=True,
        )

    def handle(self, *args, **options):
        if options["clear"]:
            clean_database()

        # Parameters for data generation
        n_patients = options["patients"]
        n_meds = options["medications"]
        n_prescriptions = options["prescriptions"]

        # Generate data
        generated_patients = generate_patients(n_patients)
        generated_meds = generate_medications(n_meds)
        generated_prescriptions = generate_prescriptions(
            n_prescriptions, generated_patients, generated_meds
        )

        # Bulk creatig of data
        created_patients = Patient.objects.bulk_create(generated_patients)
        created_meds = Medication.objects.bulk_create(generated_meds)
        created_prescriptions = Prescription.objects.bulk_create(
            generated_prescriptions
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(created_patients)} patients, "
                f"{len(created_meds)} medications and "
                f"{len(created_prescriptions)} prescriptions."
            )
        )
