import uuid
from datetime import timedelta

import factory
from factory.django import DjangoModelFactory

from medical.models import Medication, Patient, Prescription


class PatientFactory(DjangoModelFactory):
    class Meta:
        model = Patient

    id = None
    last_name = factory.Faker("last_name", locale="fr_FR")
    first_name = factory.Faker("first_name", locale="fr_FR")
    birth_date = factory.Faker("date_of_birth")


class MedicationFactory(DjangoModelFactory):
    class Meta:
        model = Medication

    id = None
    code = factory.LazyFunction(lambda: f"MED-{uuid.uuid4().hex[:8].upper()}")
    label = factory.Faker("sentence", nb_words=3)
    status = factory.Iterator([Medication.STATUS_ACTIF, Medication.STATUS_SUPPR])


class PrescriptionFactory(DjangoModelFactory):
    class Meta:
        model = Prescription

    id = None
    patient = factory.SubFactory(PatientFactory)
    medication = factory.SubFactory(MedicationFactory)
    start_date = factory.Faker("date_this_decade")
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=30))
    status = factory.Iterator(
        # STATUS_SUPPR intentionally excluded: factories create active prescriptions
        # by default. Override with PrescriptionFactory(status=STATUS_SUPPR).
        [Prescription.STATUS_VALIDE, Prescription.STATUS_EN_ATTENTE]
    )
    comment = factory.Faker("sentence", nb_words=5)
