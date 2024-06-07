from django.contrib.sessions.middleware import SessionMiddleware


def add_session_to_request(request):
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
