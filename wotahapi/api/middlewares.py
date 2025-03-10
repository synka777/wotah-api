from django.utils.deprecation import MiddlewareMixin

class AllowLocalNetworkMiddleware(MiddlewareMixin):
    def process_request(self, request):
        allowed_subnet = "192.168."
        client_ip = request.META.get("REMOTE_ADDR", "")

        if client_ip.startswith(allowed_subnet):
            request.META["HTTP_HOST"] = "allowed-host"

class CustomCORSAccessMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        ip = request.META.get("REMOTE_ADDR")

        # If the request is from 192.168.X.X subnet, allow it
        if ip.startswith("192.168."):
            response["Access-Control-Allow-Origin"] = "*"
        else:
            # Can be customized further to add stricter rules for other IPs
            response["Access-Control-Allow-Origin"] = "http://localhost:3000"  # For example, allow localhost

class CustomCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip CSRF protection if it's a safe method (like OPTIONS or GET)
        if request.method in ["GET", "OPTIONS"]:
            return None

        # Allow requests from certain subnets (like 192.168.X.X)
        ip = request.META.get("REMOTE_ADDR")
        if ip.startswith("192.168."):
            return None # Bypass CSRF check for 192.168.X.X

        # Otherwise, continue with normal CSRF protection
        return super().process_request(request)