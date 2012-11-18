import datetime

from django.conf import settings

from django.contrib.auth import logout
from django.contrib import messages


class SessionIdleTimeout:
    """
    Middleware class to timeout a session after a specified time period.
    """
    def process_request(self, request):
        if request.user.is_authenticated():
            now = datetime.datetime.now()

            last_activity = request.session.get('last_activity', now)
            since = datetime.timedelta.total_seconds(now - last_activity)
            expired = since > settings.SESSION_IDLE_TIMEOUT

            if expired:
                logout(request)
                messages.error(request, 'Your session has been timed out.')
            else:
                request.session['last_activity'] = now
        return None
