from notifications.models import Notification, NotificationType
from accounts.models import UserRole, User, Student, Course
from .models import Record
from datetime import datetime as dt
from django.contrib import messages

# new record
def newRecordAdded(request, userID, adviserID, recordID):
	user = User.objects.get(pk=userID)
	adviser = User.objects.get(pk=adviserID)
	record = Record.objects.get(pk=recordID)

	if record.record_type.pk == 1 or record.record_type.pk == 2:
		notif_type = NotificationType.objects.get(pk=3)
	elif record.record_type.pk == 3:
		notif_type = NotificationType.objects.get(pk=4)

	if user.role.name == 'Student':
		course = Student.objects.get(user=user.id).course.name
		role = UserRole.objects.get(pk=2)
	if user.role.name == 'Adviser':
		course = ''
		role = UserRole.objects.get(pk=3)
	if user.role.name == 'KTTO':
		course = ''
		role = UserRole.objects.get(pk=4)
	if user.role.name == 'RDCO':
		course = ''
		role = UserRole.objects.get(pk=5)
	if user.role.name == 'TBI':
		course = ''
		role = UserRole.objects.get(pk=7)

	notification = Notification(user=user, course=course, role=role, 
		recipient=adviser, record=record, notif_type=notif_type, 
		to_adviser=True, is_read=False, date_created=dt.now())
	
	notification.save()
	messages.success(request, "Notif sent")

# resubmission of record -> whoever decline will receive the notification
def resubmission(request, userID, recordID, checkedByID):
	user = User.objects.get(pk=userID)
	record = Record.objects.get(pk=recordID)
	recipient = User.objects.get(pk=checkedByID.checked_by.id)

	if user.role.name == 'Student':
		course = Student.objects.get(user=user.id).course.name
		role = UserRole.objects.get(pk=2)
	if user.role.name == 'Adviser':
		course = ''
		role = UserRole.objects.get(pk=3)
	if user.role.name == 'KTTO':
		course = ''
		role = UserRole.objects.get(pk=4)
	if user.role.name == 'RDCO':
		course = ''
		role = UserRole.objects.get(pk=5)
	if user.role.name == 'TBI':
		course = ''
		role = UserRole.objects.get(pk=7)

	if recipient.role.name == 'Adviser':
		to_adviser=True
		to_ktto=False 
		to_rdco=False
	if recipient.role.name == 'KTTO':
		to_adviser=False
		to_ktto=True 
		to_rdco=False
	if recipient.role.name == 'RDCO':
		to_adviser=False
		to_ktto=False 
		to_rdco=True

	notification = Notification(user=user, course=course, role=role, recipient=recipient, record=record, 
			notif_type=NotificationType.objects.get(pk=5), 
			to_adviser=to_adviser, to_ktto=to_ktto, to_rdco=to_rdco, is_read=False, date_created=dt.now())

	notification.save()
	messages.success(request, "Notif sent")

# role request approved 
def roleRequestApproved(request, userID, recipientID):
	user = User.objects.get(pk=userID)
	recipient = User.objects.get(pk=recipientID)

	if recipient.role.name == 'Student':
		to_student = True
		to_adviser = False
	if recipient.role.name == 'Adviser':
		to_adviser = True
		to_student = False

	notification = Notification(user=user, role=user.role, recipient=recipient, 
		notif_type=NotificationType.objects.get(pk=6), 
		to_adviser=to_adviser, to_student=to_student, to_ktto=True, to_rdco=True, is_read=False, date_created=dt.now())

	notification.save()
	messages.success(request, "Role Request Status sent")

# comments	
def recordComment(request, userID, recordID, recipientID):
	user = User.objects.get(pk=userID)
	record = Record.objects.get(pk=recordID)
	recipient = User.objects.get(pk=recipientID)

	if recipient.role.name == 'Student':
		to_student = True
		to_adviser=False
		to_ktto=False 
		to_rdco=False
	if recipient.role.name == 'Adviser':
		to_adviser=True
		to_ktto=False 
		to_rdco=False
		to_student = False
	if recipient.role.name == 'KTTO':
		to_adviser=False
		to_ktto=True 
		to_rdco=False
		to_student = False
	if recipient.role.name == 'RDCO':
		to_adviser=False
		to_ktto=False 
		to_rdco=True
		to_student = False

	notification = Notification(user=user, role=user.role, recipient=recipient, record=record, 
		notif_type=NotificationType.objects.get(pk=7), 
		to_adviser=to_adviser, to_ktto=to_ktto, to_rdco=to_rdco, 
		to_student=to_student, is_read=False, date_created=dt.now())

	notification.save()
	messages.success(request, "Comment sent")

# record approved or decline --> adviser first, then ktto then rdco after each approval
def recordStatus(request, userID, recordID, recipientID, status):
	user = User.objects.get(pk=userID)
	record = Record.objects.get(pk=recordID)
	recipient = User.objects.get(pk=recipientID)

	if record.record_type.pk == 1 or record.record_type.pk == 2:
		notif_type = NotificationType.objects.get(pk=3)
	elif record.record_type.pk == 3:
		notif_type = NotificationType.objects.get(pk=4)

	if status == 'approved':
		if user.role.name == 'Adviser':
			# to_ktto is true because after adviser approved is ktto
			# recipient is the representative of that record
			# user is who approved
			notification = Notification(user=user, role=user.role, record=record, 
				notif_type=notif_type, to_ktto=True, is_read=False, date_created=dt.now())
		if user.role.name == 'KTTO':
			# to_rdco is true because after ktto approved is rdco
			notification = Notification(user=user, role=user.role, record=record, 
				notif_type=notif_type, to_rdco=True, is_read=False, date_created=dt.now())
		if user.role.name == 'RDCO':
			notification = Notification(user=user, role=user.role, recipient=recipient, record=record, 
				notif_type=NotificationType.objects.get(pk=8), to_rdco=True, to_student=True, is_read=False, date_created=dt.now())
	elif status == 'declined':
		notification = Notification(user=user, role=user.role, recipient=recipient, record=record, 
			notif_type=NotificationType.objects.get(pk=9), to_student=True, is_read=False, date_created=dt.now())

	notification.save()
	messages.success(request, "Record has been approved")

