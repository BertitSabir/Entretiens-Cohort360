from django.contrib import admin

from .models import Medication, Patient, Prescription


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["id", "last_name", "first_name", "birth_date"]
    search_fields = ["last_name", "first_name"]
    ordering = ["id"]
    list_per_page = 25


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "label", "status"]
    list_filter = ["status"]
    search_fields = ["code", "label"]
    ordering = ["id"]
    list_per_page = 25


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "patient",
        "medication",
        "status",
        "start_date",
        "end_date",
        "created_at",
    ]
    list_filter = ["status"]
    search_fields = ["patient__last_name", "patient__first_name", "medication__code"]
    autocomplete_fields = ["patient", "medication"]
    readonly_fields = ["created_at"]
    ordering = ["id"]
    list_select_related = ["patient", "medication"]
    date_hierarchy = "created_at"
    list_per_page = 25
