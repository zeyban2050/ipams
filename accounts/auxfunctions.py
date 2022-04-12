from notifications.models import Notification, NotificationType
from .models import UserRole, User, Student
from datetime import datetime as dt
from django.contrib import messages

# request to be student method
def roleRequestStudent(request, userID, course):
	user = User.objects.get(pk=userID)
	print(user.first_name)

	notification = Notification(user=user, course=course, role=UserRole.objects.get(pk=2), 
		to_adviser=True, to_ktto=True, to_rdco=True, notif_type=NotificationType.objects.get(pk=1), is_read=False, date_created=dt.now())
	
	notification.save()
	messages.success(request, "Role Request to be a student sent")

# request to be adviser method
def roleRequestAdviser(request, userID):
	user = User.objects.get(pk=userID)
	print(user.first_name)

	notification = Notification(user=user, role=UserRole.objects.get(pk=3), 
		to_adviser=True, to_ktto=True, to_rdco=True, notif_type=NotificationType.objects.get(pk=2), is_read=False, date_created=dt.now())

	notification.save()
	messages.success(request, "Role Request to be an adviser sent")