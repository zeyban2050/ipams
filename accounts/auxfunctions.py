from notifications.models import Notification, NotificationType
from .models import UserRole, User, Student
from datetime import datetime as dt
from django.contrib import messages

from django.core.mail import send_mail, send_mass_mail
from django.db.models import Subquery, Q
from ipams import settings

# request to be student method
def roleRequestStudent(request, userID, course):
	user = User.objects.get(pk=userID)
	print(user.first_name)

	notification = Notification(user=user, course=course, role=UserRole.objects.get(pk=2), 
		to_ktto=True, to_rdco=True, notif_type=NotificationType.objects.get(pk=1), is_read=False, date_created=dt.now())
	
	notification.save()
	messages.success(request, "Role Request to be a student sent")

	url = request.build_absolute_uri()
	base_url = url.split("account/signup")
	redirect_path = base_url[0]

	kart_accounts = User.objects.filter(Q(role__in=Subquery(UserRole.objects.filter(pk=3).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=7).values('pk'))))

	mail_subject = NotificationType.objects.get(pk=1)
	message = (
		f' {user.first_name} {user.last_name} created an account and requested to be a Student under the program {user.student.course.name}.' \
		f' \nTo accept the role request of the user, login to the website {redirect_path}.'
	)

	messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in kart_accounts]
	send_mass_mail(messages_to_send) 

# request to be adviser method
def roleRequestAdviser(request, userID):
	user = User.objects.get(pk=userID)
	print(user.first_name)

	notification = Notification(user=user, role=UserRole.objects.get(pk=3), 
		to_ktto=True, to_rdco=True, notif_type=NotificationType.objects.get(pk=2), is_read=False, date_created=dt.now())

	notification.save()
	messages.success(request, "Role Request to be an adviser sent")

	url = request.build_absolute_uri()
	base_url = url.split("account/signup")
	redirect_path = base_url[0]

	kart_accounts = User.objects.filter(Q(role__in=Subquery(UserRole.objects.filter(pk=3).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=7).values('pk'))))
	
	mail_subject = NotificationType.objects.get(pk=1)
	message = (
		f' {user.first_name} {user.last_name} created an account and requested to be an Adviser' \
		f' under the department of {user.adviser.department.name} and college of {user.adviser.college.name}.' \
		f' \nTo accept the role request of the user, login to the website {redirect_path}.'
	)

	messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in kart_accounts]
	send_mass_mail(messages_to_send)