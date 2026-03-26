import random
import string
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from medical.models import Medication, Patient, Prescription


def random_date(start_year=1940, end_year=2025):
    start_dt = date(start_year, 1, 1)
    end_dt = date(end_year, 12, 31)
    days = (end_dt - start_dt).days
    return start_dt + timedelta(days=random.randint(0, days))


class Command(BaseCommand):
    help = "Seed the database with demo Patients, Medications, and Prescriptions"

    def add_arguments(self, parser):
        parser.add_argument("--patients", type=int, default=10)
        parser.add_argument("--medications", type=int, default=5)
        parser.add_argument("--prescriptions", type=int, default=30)

    def handle(self, *args, **options):
        # Clear existing data to avoid duplicates on multiple runs
        Prescription.objects.all().delete()
        Patient.objects.all().delete()
        Medication.objects.all().delete()

        # Parameters for data generation
        n_patients = options["patients"]
        n_meds = options["medications"]
        n_prescriptions = options["prescriptions"]

        last_names = [
            "Martin",
            "Bernard",
            "Thomas",
            "Petit",
            "Robert",
            "Richard",
            "Durand",
            "Dubois",
            "Moreau",
            "Laurent",
            "Michel",
            "Garcia",
            "David",
            "Bertrand",
            "Roux",
            "Vincent",
            "Fournier",
            "Morel",
            "Lefebvre",
            "Mercier",
            "Dupont",
            "Lambert",
            "Bonnet",
            "Francois",
            "Martinez",
            "Legrand",
            "Garnier",
            "Faure",
            "Andre",
            "Rousseau",
            "Simon",
            "Leroy",
            "Roux",
            "Girard",
            "Colin",
            "Lefevre",
            "Boyer",
            "Chevalier",
            "Robin",
            "Masson",
            "Picard",
            "Blanc",
            "Gautier",
            "Nicolas",
            "Henry",
            "Perrin",
            "Morin",
            "Mathieu",
            "Clement",
            "Gauthier",
            "Dumont",
            "Lopez",
            "Fontaine",
            "Schmitt",
            "Rodriguez",
            "Dufour",
            "Blanchard",
            "Meunier",
            "Brunet",
            "Roy",
        ]
        first_names = [
            "Jean",
            "Jeanne",
            "Marie",
            "Luc",
            "Lucie",
            "Paul",
            "Camille",
            "Pierre",
            "Sophie",
            "Emma",
            "Louis",
            "Louise",
            "Alice",
            "Gabriel",
            "Jules",
            "Lucas",
            "Hugo",
            "Arthur",
            "Adam",
            "Raphael",
            "Leo",
            "Nathan",
            "Tom",
            "Zoe",
            "Chloe",
            "Ines",
            "Lea",
            "Lena",
            "Eva",
            "Nina",
            "Ethan",
            "Noah",
            "Liam",
            "Rose",
            "Anna",
            "Jade",
            "Maeva",
            "Sarah",
            "Laura",
            "Clara",
            "Julie",
            "Nicolas",
            "Thomas",
            "Antoine",
            "Emilie",
            "Mathilde",
            "Charlotte",
            "Manon",
            "Julia",
            "Elise",
            "Victor",
            "Alex",
            "Samuel",
            "Valentin",
            "Axel",
            "Simon",
            "Romain",
            "Vincent",
            "Marc",
            "David",
        ]

        created_patients = []
        for _ in range(n_patients):
            p = Patient.objects.create(
                last_name=random.choice(last_names),
                first_name=random.choice(first_names),
                birth_date=random_date(),
            )
            created_patients.append(p)

        base_labels = [
            "Paracetamol",
            "Ibuprofen",
            "Amoxicillin",
            "Aspirin",
            "Omeprazole",
            "Metformin",
            "Loratadine",
            "Cetirizine",
            "Azithromycin",
            "Atorvastatin",
            "Simvastatin",
            "Lisinopril",
            "Amlodipine",
            "Metoprolol",
            "Sertraline",
            "Fluoxetine",
            "Escitalopram",
            "Gabapentin",
            "Pregabalin",
            "Tramadol",
            "Oxycodone",
            "Hydrocodone",
            "Morphine",
            "Diazepam",
            "Alprazolam",
            "Clonazepam",
            "Zolpidem",
            "Trazodone",
            "Cyclobenzaprine",
            "Meloxicam",
            "Prednisone",
            "Methylprednisolone",
            "Hydrocortisone",
            "Fluticasone",
            "Montelukast",
            "Albuterol",
            "Fluconazole",
            "Terbinafine",
            "Metronidazole",
            "Ciprofloxacin",
            "Doxycycline",
            "Cephalexin",
            "Nitrofurantoin",
            "Pantoprazole",
            "Ranitidine",
            "Famotidine",
            "Dicyclomine",
            "Ondansetron",
            "Promethazine",
            "Meclizine",
        ]
        doses = [15, 20, 25, 50, 100, 200, 250, 300, 400, 500, 800, 1000]
        created_meds = []
        for i in range(n_meds):
            code = f"MED{i:04d}{random.choice(string.ascii_uppercase)}"
            label = (
                f"{random.choice(base_labels)} {random.choice(doses)}"
                + random.choice(["mg", "g", "µg"])
            )
            status = random.choices(
                [Medication.STATUS_ACTIF, Medication.STATUS_SUPPR], weights=[0.8, 0.2]
            )[0]
            m = Medication.objects.create(code=code, label=label, status=status)
            created_meds.append(m)

        statuses = [
            Prescription.STATUS_VALIDE,
            Prescription.STATUS_EN_ATTENTE,
            Prescription.STATUS_SUPPR,
        ]
        created_prescriptions = []
        for _ in range(n_prescriptions):
            start = random_date(start_year=2022, end_year=2025)
            end = start + timedelta(days=random.randint(1, 365))
            p = Prescription.objects.create(
                patient=random.choice(created_patients),
                medication=random.choice(created_meds),
                start_date=start,
                end_date=end,
                status=random.choices(statuses, weights=[0.6, 0.3, 0.1])[0],
                comment=random.choice(
                    [
                        "",
                        "",
                        "",  # majorité sans commentaire
                        "Renouvellement mensuel",
                        "Prendre au repas",
                        "Allergie pénicilline — surveiller",
                        "Posologie réduite pour insuffisance rénale",
                    ]
                ),
            )
            created_prescriptions.append(p)

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(created_patients)} patients, "
                f"{len(created_meds)} medications and "
                f"{len(created_prescriptions)} prescriptions."
            )
        )
