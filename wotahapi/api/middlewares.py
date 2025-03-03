from django.utils.deprecation import MiddlewareMixin

class AllowLocalNetworkMiddleware(MiddlewareMixin):
    def process_request(self, request):
        allowed_subnet = "192.168."
        client_ip = request.META.get("REMOTE_ADDR", "")

        if client_ip.startswith(allowed_subnet):
            request.META["HTTP_HOST"] = "allowed-host"