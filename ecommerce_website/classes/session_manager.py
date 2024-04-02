from django.contrib.sessions.models import Session
from django.utils import timezone

class SessionManager:
    @staticmethod
    def clear_session(request):
        request.session.clear()
