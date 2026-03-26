from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # ProtectedError is not currently reachable via the API since Patient and Medication
    # are read-only. This handler is kept as a safeguard for future writable endpoints.
    response = exception_handler(exc, context)
    if isinstance(exc, ProtectedError):
        return Response(
            {
                "error": "Cannot delete this record because it is referenced "
                "by existing prescriptions."
            },
            status=status.HTTP_409_CONFLICT,
        )
    return response
