from notifications.models import Notification, NotificationType
from accounts.models import UserRole, User, Student, Course
from .models import Record
from datetime import datetime as dt
from django.contrib import messages
from django.db.models import Subquery, Q
from django.core.mail import send_mail, send_mass_mail
from ipams import settings

# Connecting to Google Cloud Storage
# from google.cloud import storage
# def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     """Uploads a file to the bucket."""
#     # The ID of your GCS bucket
#     # bucket_name = "your-bucket-name"
#     # The path to your file to upload
#     # source_file_name = "local/path/to/file"
#     # The ID of your GCS object
#     # destination_blob_name = "storage-object-name"
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)
#     f = source_file_name.open()
#     media_content = f.read()
#     # blob.upload_from_filename(media_content)
#     blob.upload_from_string(media_content)
#     print(
#         "File {} uploaded to {}.".format(
#             source_file_name, destination_blob_name
#         )
#     )

# def download_blob(bucket_name, source_blob_name):
# 	"""Downloads a blob from the bucket."""
# 	# The ID of your GCS bucket
# 	# bucket_name = "your-bucket-name"
# 	# The ID of your GCS object
# 	# source_blob_name = "storage-object-name"
# 	# The path to which the file should be downloaded
# 	# destination_file_name = "local/path/to/file"
# 	storage_client = storage.Client()
# 	bucket = storage_client.bucket(bucket_name)
# 	# Construct a client side representation of a blob.
# 	# Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
# 	# any content from Google Cloud Storage. As we don't need additional data,
# 	# using `Bucket.blob` is preferred here.
# 	# blob = bucket.blob(source_blob_name)
# 	blob = bucket.get_blob(source_blob_name)
# 	print(blob.media_link)
# 	return blob.media_link

# def delete_blob(bucket_name, blob_name):
#     """Deletes a blob from the bucket."""
#     # bucket_name = "your-bucket-name"
#     # blob_name = "your-object-name"

#     storage_client = storage.Client()

#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(blob_name)
#     blob.delete()

#     print("Blob {} deleted.".format(blob_name))

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

	notification = Notification(user=user, course=course, role=role, recipient=adviser, record=record, notif_type=notif_type, 
		is_read=False, date_created=dt.now())
	
	notification.save()

	url = request.build_absolute_uri()
	base_url = url.split("add")
	redirect_path = base_url[0] + 'record/pending/' + str(record.pk)

	mail_subject = notif_type
	message = (
		f'{user.first_name} {user.last_name} has submitted a new record entitled {record.title}' \
		f' with the classification of {record.classification} and a PSCED classification of' \
		f' {record.psced_classification} on {record.date_created.strftime("%m/%d/%Y %H:%M")}.' \
		f'\nTo view the record, login to the website {redirect_path}'
	)
	to_email = adviser.email
	send_mail(
	    mail_subject, 
	    message, 
	    settings.EMAIL_HOST_USER, 
	    [to_email],
	    fail_silently=False
	)

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

	notification = Notification(user=user, course=course, role=role, recipient=recipient, record=record, 
			notif_type=NotificationType.objects.get(pk=5), is_read=False, date_created=dt.now())

	notification.save()

	url = request.build_absolute_uri()
	base_url = url.split("add")
	redirect_path = base_url[0] + 'record/pending/' + str(record.pk)

	mail_subject = NotificationType.objects.get(pk=5)
	message = (
		f"{user.first_name} {user.last_name} has resubmitted the record {record.title}" \
		f' under the classification of {record.classification} and a PSCED classification of' \
		f' {record.psced_classification} on {record.date_created.strftime("%m/%d/%Y %H:%M")}.' \
		f'\nTo view the record, login to the website {redirect_path}'
	)
	to_email = recipient.email
	send_mail(
	    mail_subject, 
	    message, 
	    settings.EMAIL_HOST_USER, 
	    [to_email],
	    fail_silently=False
	)


# role request approved 
def roleRequestApproved(request, userID, recipientID):
	user = User.objects.get(pk=userID)
	recipient = User.objects.get(pk=recipientID)

	notification = Notification(user=user, role=user.role, recipient=recipient, 
		notif_type=NotificationType.objects.get(pk=6), to_ktto=True, to_rdco=True, is_read=False, date_created=dt.now())

	notification.save()

	url = request.build_absolute_uri()
	base_url = url.split("account/signup")
	redirect_path = base_url[0]

	karts_accounts = User.objects.filter(Q(pk=recipient.pk) | Q(role__in=Subquery(UserRole.objects.filter(pk=3).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=7).values('pk'))))
	
	mail_subject = NotificationType.objects.get(pk=6)
	message = (
		f"{user.first_name} {user.last_name} approved {recipient.first_name} {recipient.last_name}'s request to be a {recipient.role}." \
		f' \nLogin to the website {redirect_path} for more information.'
	)

	messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in karts_accounts]
	send_mass_mail(messages_to_send) 

# comments	
def recordComment(request, userID, recordID, recipientID):
	user = User.objects.get(pk=userID)
	record = Record.objects.get(pk=recordID)
	recipient = User.objects.get(pk=recipientID)

	notification = Notification(user=user, role=user.role, recipient=recipient, record=record, 
		notif_type=NotificationType.objects.get(pk=7), is_read=False, date_created=dt.now())

	notification.save()

# record approved or decline --> adviser first, then ktto then rdco after each approval
def recordStatus(request, userID, recordID, recipientID, status):
	user = User.objects.get(pk=userID)
	record = Record.objects.get(pk=recordID)
	recipient = User.objects.get(pk=recipientID)

	if record.record_type.pk == 1 or record.record_type.pk == 2:
		notif_type = NotificationType.objects.get(pk=3)
	elif record.record_type.pk == 3:
		notif_type = NotificationType.objects.get(pk=4)

	# redirect_path = request.build_absolute_uri('record/pending/' + str(record.pk))
	redirect_path = request.build_absolute_uri()

	if status == 'approved':
		if user.role.name == 'Adviser':
			# to_ktto is true because after adviser approved is ktto
			# recipient is the representative of that record
			# user is who approved
			notification = Notification(user=user, role=user.role, record=record, 
				notif_type=notif_type, to_ktto=True, is_read=False, date_created=dt.now())

			ktto_accounts = User.objects.filter(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk')))

			mail_subject = notif_type
			message = (
				f'{user.first_name} {user.last_name} has approved the record {record.title}' \
				f' with a classification of {record.classification} and a PSCED classification of' \
				f' {record.psced_classification} today.' \
				f'\nTo view the record, login to the website {redirect_path}'
			)
			
			messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in ktto_accounts]
			send_mass_mail(messages_to_send) 
			
		if user.role.name == 'KTTO' or user.role.name == 'TBI':
			# to_rdco is true because after ktto approved is rdco
			notification = Notification(user=user, role=user.role, record=record, 
				notif_type=notif_type, to_rdco=True, is_read=False, date_created=dt.now())

			rdco_accounts = User.objects.filter(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk')))

			mail_subject = notif_type
			message = (
				f'{user.first_name} {user.last_name} has approved the record {record.title}' \
				f' with a classification of {record.classification} and a PSCED classification of' \
				f' {record.psced_classification} today.' \
				f'\nTo view the record, login to the website {redirect_path}'
			)
			
			messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in rdco_accounts]
			send_mass_mail(messages_to_send) 

		if user.role.name == 'RDCO':
			notification = Notification(user=user, role=user.role, recipient=recipient, record=record, 
				notif_type=NotificationType.objects.get(pk=8), is_read=False, date_created=dt.now())

			mail_subject = NotificationType.objects.get(pk=8)
			message = (
				f'{user.first_name} {user.last_name} has approved the record {record.title}' \
				f' with a classification of {record.classification} and a PSCED classification of' \
				f' {record.psced_classification} today.' \
				f'\nTo view the record, login to the website {redirect_path}'
			)
			to_email = recipient.email
			send_mail(
			    mail_subject, 
			    message, 
			    settings.EMAIL_HOST_USER, 
			    [to_email],
			    fail_silently=False
			)

	elif status == 'declined':
		notification = Notification(user=user, role=user.role, recipient=recipient, record=record, 
			notif_type=NotificationType.objects.get(pk=9), is_read=False, date_created=dt.now())

		mail_subject = NotificationType.objects.get(pk=9)
		message = (
			f'{user.first_name} {user.last_name} has declined the record {record.title}' \
			f' with a classification of {record.classification} and a PSCED classification of' \
			f' {record.psced_classification} today.' \
			f'\nTo edit and resubmit the record, login to the website {redirect_path}'
		)
		to_email = recipient.email
		send_mail(
		    mail_subject, 
		    message, 
		    settings.EMAIL_HOST_USER, 
		    [to_email],
		    fail_silently=False
		)

	notification.save()

def deleteRecord(request, userID, recordID, reason): #Only the admins can approve to delete a record
	user = User.objects.get(pk=userID)
	record = Record.objects.get(pk=recordID)

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

	notification = Notification(user=user, course=course, role=role, record=record, notif_type=NotificationType.objects.get(pk=10), 
		to_ktto=True, to_rdco=True, is_read=False, date_created=dt.now())
	
	notification.save()

	url = request.build_absolute_uri()
	base_url = url.split("record/")
	redirect_path = base_url[0] + 'records/pending/'

	kr_accounts = User.objects.filter(Q(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk'))))

	mail_subject = NotificationType.objects.get(pk=10)
	message = (
		f'{user.first_name} {user.last_name} has requested the approval to delete the record {record.title}' \
		f' with a classification of {record.classification} and a PSCED classification of' \
		f' {record.psced_classification} with the reasoning {reason}.' \
		f'\nTo approve the request, login to the website and go to {redirect_path}'
	)
	
	messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in kr_accounts]
	send_mass_mail(messages_to_send) 


def approvedDeleteRecord(request, userID, recordID, recipientID, reason):
	user = User.objects.get(pk=userID) # the admin who approved the request
	record = Record.objects.get(pk=recordID)
	recipient = User.objects.get(pk=recipientID) #the user who requested for approval to delete a record

	notification = Notification(user=user, role=user.role, recipient=recipient, record=record,
		notif_type=NotificationType.objects.get(pk=11), to_ktto=True, to_rdco=True, is_read=False, date_created=dt.now())

	notification.save()

	mail_subject = NotificationType.objects.get(pk=11)
	url = request.build_absolute_uri()
	base_url = url.split("record/")
	redirect_path = base_url[0] + 'records/pending/'

	# to admins who would approved the request
	# kr_accounts = User.objects.filter(Q(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk'))))
	# message = (
	# 	f'{user.first_name} {user.last_name} has approved the request of {recipient.first_name} {recipient.last_name} to delete the record {record.title}' \
	# 	f' with a classification of {record.classification} and a PSCED classification of' \
	# 	f' {record.psced_classification} with the reasoning {reason}. \n\nThe record has been automatically deleted.' \
	# 	f'\nTo approve other requests, login to the website {redirect_path}'
	# )	
	# messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in kr_accounts]
	# send_mass_mail(messages_to_send) 

	# for whoever sent the request that got approved
	message = (
		f'{user.first_name} {user.last_name} has approved your request to delete the record {record.title}' \
		f' with a classification of {record.classification} and a PSCED classification of' \
		f' {record.psced_classification} with the reasoning {reason}. \n\nThe record has been automatically deleted.' \
		f'\nFor more information, login to the website {redirect_path}'
	)
	to_email = recipient.email
	send_mail(
	    mail_subject, 
	    message, 
	    settings.EMAIL_HOST_USER, 
	    [to_email],
	    fail_silently=False
	)


def sendDownloadRequest(request, userID, recordID):
	user = User.objects.get(pk=userID) # the user who sent a request
	record = Record.objects.get(pk=recordID)
	
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

	notification = Notification(user=user, course=course, role=role, record=record, notif_type=NotificationType.objects.get(pk=12), 
		to_ktto=True, to_rdco=True, is_read=False, date_created=dt.now())
	
	notification.save()
	
	url = request.build_absolute_uri()
	base_url = url.split("record/")
	redirect_path = base_url[0] + 'records/pending/'

	kr_accounts = User.objects.filter(Q(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk'))))

	mail_subject = NotificationType.objects.get(pk=10)
	message = (
		f'{user.first_name} {user.last_name} has sent a request to download record {record.title}' \
		f' with a classification of {record.classification} and a PSCED classification of' \
		f' {record.psced_classification}.' \
		f'\nTo approve the request, login to the website and go to {redirect_path}'
	)
	
	messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in kr_accounts]
	send_mass_mail(messages_to_send)


def approvedDownloadRequest(request, userID, recordID, recipientID):
	user = User.objects.get(pk=userID) # the admin who approved the request
	record = Record.objects.get(pk=recordID)
	recipient = User.objects.get(pk=recipientID) #the user who requested for approval to delete a record

	notification = Notification(user=user, role=user.role, recipient=recipient, record=record,
		notif_type=NotificationType.objects.get(pk=13), to_ktto=True, to_rdco=True, is_read=False, date_created=dt.now())

	notification.save()
	
	mail_subject = NotificationType.objects.get(pk=13)
	
	url = request.build_absolute_uri()
	# base_url = url.split("approved/")
	# redirect_path = base_url[0] + 'records/pending/'
	# # to admins who would approved the request
	# kr_accounts = User.objects.filter(Q(role__in=Subquery(UserRole.objects.filter(pk=5).values('pk'))) | Q(role__in=Subquery(UserRole.objects.filter(pk=4).values('pk'))))
	# message = (
	# 	f'{user.first_name} {user.last_name} has approved the request of {recipient.first_name} {recipient.last_name} to download the record {record.title}' \
	# 	f'\nTo approve other requests, login to the website {redirect_path}'
	# )
	# messages_to_send = [(mail_subject, message, settings.EMAIL_HOST_USER, [account.email]) for account in kr_accounts]
	# send_mass_mail(messages_to_send) 

	base_url = url.split("approved/")
	http_cut = base_url[0].split("//")
	print(http_cut[0])
	# redirect_path_download = base_url[0] + 'download/abstract/' + recordID
	if http_cut[0] == 'http:':
		redirect_path_download = 'http://' + http_cut[1] + 'download/abstract/' + recordID
	elif http_cut[0] == 'https:':
		redirect_path_download = 'https://' + http_cut[1] + 'download/abstract/' + recordID

	# for whoever sent the request that got approved
	message = (
		f'{user.first_name} {user.last_name} has approved your request to download the record {record.title}' \
		f'\nClick the link and the download will start automatically. {redirect_path_download}'
	)
	to_email = recipient.email
	send_mail(
	    mail_subject, 
	    message, 
	    settings.EMAIL_HOST_USER, 
	    [to_email],
	    fail_silently=False
	)

