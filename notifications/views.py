from django.shortcuts import render
from django.views import View
from notifications.models import Notification


class NotificationsHomeView(View):
    name = 'notifications/index.html'

    def get(self, request):
        user = request.user
        received_notifications = Notification.objects.filter(recipient=user)
        context = {
            'received_notifications': received_notifications,
        }
        return render(request, self.name, context)