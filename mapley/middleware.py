from django.shortcuts import render
from django.contrib.auth import logout
from django.utils import timezone

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the error
        print(f"An error occurred: {exception}")
        
        # Render a custom error page
        return render(request, 'error.html', {'error': str(exception)}, status=500)

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                inactive_time = timezone.now() - timezone.datetime.fromtimestamp(last_activity)
                if inactive_time.total_seconds() > 1800:  # 30 minutes
                    logout(request)
            request.session['last_activity'] = timezone.now().timestamp()

        response = self.get_response(request)
        return response    