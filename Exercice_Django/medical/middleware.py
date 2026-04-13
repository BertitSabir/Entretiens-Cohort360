class DeprecationMiddleware:
    """Adds deprecation headers on legacy (unversioned) routes."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/"):
            response["Deprecation"] = "true"
            response["Sunset"] = "2027-01-01"
            response["Link"] = '</api/v1/>; rel="successor-version"'
        return response
