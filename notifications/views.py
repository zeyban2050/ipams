from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import authorized_roles, authorized_record_user
from django.db.models import Count, Subquery, Q, Sum

from accounts.models import User, Student, Course, UserRecord, UserRole, RoleRequest
from records.models import CheckedRecord
from .models import *
from notifications.auxfunctions import filterHelper, listOfAuthors

class StudentNotification(View):
    name = 'notifications/student_notification_page.html'
    def get(self, request):
        user = request.user
        print(user.id)
        notifications = Notification.objects.filter(recipient=user.id)
        request.session['notif_count'] = notifications.count()
        print(notifications)
        context = {
            'notifications': notifications,
            'category': 'Filter',
        }
        return render(request, self.name, context)
    def post(self, request):
        if request.method == 'POST':
            user = request.user
            # for filter
            if 'all' in request.POST:
                notifications = Notification.objects.filter(recipient=user.id)
                return render(request, self.name, filterHelper(request, notifications, 'ALL'))
            if 'read' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(is_read=True))
                return render(request, self.name, filterHelper(request, notifications, 'Read'))
            if 'unread' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(is_read=False))
                return render(request, self.name, filterHelper(request, notifications, 'Unread'))
            if 'approved' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(notif_type=NotificationType.objects.get(pk=8)))
                return render(request, self.name, filterHelper(request, notifications, 'Approved'))
            if 'declined' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(notif_type=NotificationType.objects.get(pk=9)))
                return render(request, self.name, filterHelper(request, notifications, 'Declined'))

            if request.POST.get('removeNotification'):
                idList = request.POST.getlist('listOfID[]')
                for id in idList:
                    Notification.objects.get(pk=id).delete()
                return JsonResponse({'success': True})

            if request.POST.get('roleChange'):
                role = request.POST.get('role')
                User.objects.filter(pk=id).update(role=UserRole.objects.get(name=role))
                removeRequest = RoleRequest.objects.get(user=User.objects.get(pk=id))
                removeRequest.delete()
                return JsonResponse({'success': True})

            # content for each notification -> 2nd box content
            id = request.POST.get('notifID')
            print(id)
            Notification.objects.filter(pk=id).update(is_read=True)
            notifications = Notification.objects.filter(recipient=user.id)
            request.session['notif_count'] = notifications.count()
            
            notif = Notification.objects.get(pk=id)
            if notif.notif_type.name == 'Record Approved' or notif.notif_type.name == 'Record Declined':
                record_status = CheckedRecord.objects.filter(record=notif.record.id).latest('status')
                return JsonResponse({'success': True,
                                    'date': notif.date_created,
                                    'subject': notif.notif_type.name,
                                    'title': notif.record.title,
                                    'classification': notif.record.classification.name,
                                    'psced': notif.record.psced_classification.name,
                                    'recordID': notif.record.id,
                                    'status': record_status.status,
                                    'subject-body':notif.notif_type.name+' by '+notif.user.first_name+notif.user.last_name,
                                    'checked-by': notif.user.first_name+' '+notif.user.last_name,
                                    'authors': listOfAuthors(request, notif.record.id)})
            elif notif.notif_type.name == 'Role Request Approved':
                return JsonResponse({'success': True,
                                    'fname': notif.recipient.first_name,
                                    'mname': notif.recipient.middle_name,
                                    'lname': notif.recipient.last_name,
                                    'username': notif.recipient.username,
                                    'email': notif.recipient.email,
                                    'date': notif.date_created,
                                    'subject': notif.notif_type.name,
                                    'request': request,
                                    'subject-body':notif.notif_type.name+' by '+notif.user.first_name+notif.user.last_name,
                                    'approved-by': notif.user.first_name+' '+notif.user.last_name})

class AdviserNotification(View):
    name = 'notifications/adviser_notification_page.html'
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(Q(recipient=user.id) | Q(notif_type=NotificationType.objects.get(pk=6)) | Q(notif_type=NotificationType.objects.get(pk=1)) | Q(notif_type=NotificationType.objects.get(pk=2)))
        request.session['notif_count'] = notifications.count()
        print(notifications)
        context = {
            'notifications': notifications,
            'category': 'Filter',
        } 
        return render(request, self.name, context)
    def post(self, request):
        if request.method == 'POST':
            user = request.user
            # for filter
            if 'all' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) | Q(notif_type=NotificationType.objects.get(pk=6)) | Q(notif_type=NotificationType.objects.get(pk=1)) | Q(notif_type=NotificationType.objects.get(pk=2)))
                return render(request, self.name, filterHelper(request, notifications, 'ALL'))
            if 'read' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(is_read=True))
                return render(request, self.name, filterHelper(request, notifications, 'Read'))
            if 'unread' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(is_read=False))
                return render(request, self.name, filterHelper(request, notifications, 'Unread'))
            if 'rrs' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(notif_type=NotificationType.objects.get(pk=1)))
                return render(request, self.name, filterHelper(request, notifications, 'Role Request Student'))
            if 'rra' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(notif_type=NotificationType.objects.get(pk=2)))
                return render(request, self.name, filterHelper(request, notifications, 'Role Request Adviser'))
            if 'nrpt' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(notif_type=NotificationType.objects.get(pk=3)))
                return render(request, self.name, filterHelper(request, notifications, 'New Record Proposal/Thesis'))
            if 'nrp' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(notif_type=NotificationType.objects.get(pk=4)))
                return render(request, self.name, filterHelper(request, notifications, 'New Record Project'))
            if 'resubmission' in request.POST:
                notifications = Notification.objects.filter(Q(recipient=user.id) & Q(notif_type=NotificationType.objects.get(pk=5)))
                return render(request, self.name, filterHelper(request, notifications, 'Resubmissions'))

            if request.POST.get('removeNotification'):
                idList = request.POST.getlist('listOfID[]')
                for id in idList:
                    Notification.objects.get(pk=id).delete()
                return JsonResponse({'success': True})

            if request.POST.get('roleChange'):
                role = request.POST.get('role')
                User.objects.filter(pk=id).update(role=UserRole.objects.get(name=role))
                removeRequest = RoleRequest.objects.get(user=User.objects.get(pk=id))
                removeRequest.delete()
                return JsonResponse({'success': True})

            id = request.POST.get('notifID')
            Notification.objects.filter(pk=id).update(is_read=True)
            notifications = Notification.objects.filter(Q(recipient=user.id) | Q(notif_type=NotificationType.objects.get(pk=6)) | Q(notif_type=NotificationType.objects.get(pk=1)) | Q(notif_type=NotificationType.objects.get(pk=2)))
            request.session['notif_count'] = notifications.count()
            notif = Notification.objects.get(pk=id)
            if notif.notif_type.name == 'Role Request Student' or notif.notif_type.name == 'Role Request Adviser':
                return JsonResponse({'success': True,
                                    'fname': notif.user.first_name,
                                    'mname': notif.user.middle_name,
                                    'lname': notif.user.last_name,
                                    'username': notif.user.username,
                                    'email': notif.user.email,
                                    'course': notif.course,
                                    'date': notif.date_created,
                                    'subject': notif.notif_type.name,
                                    'id': notif.user.id,
                                    'role': notif.user.role.name})
            elif notif.notif_type.name == 'Role Request Approved':
                if notif.recipient.role.name == 'Student':
                    request = "Role Request Student"
                elif notif.recipient.role.name == 'Adviser':
                    request = "Role Request Adviser"
                return JsonResponse({'success': True,
                                    'fname': notif.recipient.first_name,
                                    'mname': notif.recipient.middle_name, 
                                    'lname': notif.recipient.last_name,
                                    'username': notif.recipient.username,
                                    'email': notif.recipient.email,
                                    'date': notif.date_created,
                                    'subject': notif.notif_type.name,
                                    'request': request,
                                    'subject-body':notif.notif_type.name+' by '+notif.user.first_name+notif.user.last_name,
                                    'approved-by': notif.user.first_name+' '+notif.user.last_name})
            elif notif.notif_type.name == 'New Record Proposal/Thesis' or notif.notif_type.name == 'New Record Project' or notif.notif_type.name == 'Resubmission':
                return JsonResponse({'success': True,
                                    'date': notif.date_created,
                                    'subject': notif.notif_type.name,
                                    'title': notif.record.title,
                                    'classification': notif.record.classification.name,
                                    'psced': notif.record.psced_classification.name,
                                    'recordID': notif.record.id,
                                    'authors': listOfAuthors(request, notif.record.id)})

class KTTONotification(View):
    name = 'notifications/ktto_notification_page.html'
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(Q(to_ktto=True) | Q(recipient=user.id))
        request.session['notif_count'] = notifications.count()
        print(notifications)
        context = {
            'notifications': notifications,
            'category': 'Filter',
        } 
        return render(request, self.name, context)
    def post(self, request):
        if request.method == 'POST':
            user = request.user
            # for filter
            if 'all' in request.POST:
                notifications = Notification.objects.filter(Q(to_ktto=True) | Q(recipient=user.id))
                return render(request, self.name, filterHelper(request, notifications, 'ALL'))
            if 'read' in request.POST:
                notifications = Notification.objects.filter((Q(to_ktto=True) | Q(recipient=user.id)) & Q(is_read=True))
                return render(request, self.name, filterHelper(request, notifications, 'Read'))
            if 'unread' in request.POST:
                notifications = Notification.objects.filter((Q(to_ktto=True) | Q(recipient=user.id)) & Q(is_read=False))
                return render(request, self.name, filterHelper(request, notifications, 'Unread'))
            if 'rrs' in request.POST:
                notifications = Notification.objects.filter((Q(to_ktto=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=1)))
                return render(request, self.name, filterHelper(request, notifications, 'Role Request Student'))
            if 'rra' in request.POST:
                notifications = Notification.objects.filter((Q(to_ktto=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=2)))
                return render(request, self.name, filterHelper(request, notifications, 'Role Request Adviser'))
            if 'nrpt' in request.POST:
                notifications = Notification.objects.filter((Q(to_ktto=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=3)))
                return render(request, self.name, filterHelper(request, notifications, 'New Record Proposal/Thesis'))
            if 'nrp' in request.POST:
                notifications = Notification.objects.filter((Q(to_ktto=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=4)))
                return render(request, self.name, filterHelper(request, notifications, 'New Record Project'))
            if 'resubmission' in request.POST:
                notifications = Notification.objects.filter((Q(to_ktto=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=5)))
                return render(request, self.name, filterHelper(request, notifications, 'Resubmissions'))

            if request.POST.get('removeNotification'):
                idList = request.POST.getlist('listOfID[]')
                for id in idList:
                    Notification.objects.get(pk=id).delete()
                return JsonResponse({'success': True})

            if request.POST.get('roleChange'):
                role = request.POST.get('role')
                User.objects.filter(pk=id).update(role=UserRole.objects.get(name=role))
                removeRequest = RoleRequest.objects.get(user=User.objects.get(pk=id))
                removeRequest.delete()
                return JsonResponse({'success': True})

            # content for each notification -> 2nd box content
            if request.POST.get('displayContent'):
                id = request.POST.get('notifID')
                Notification.objects.filter(pk=id).update(is_read=True)
                notifications = Notification.objects.filter(Q(to_ktto=True) | Q(recipient=user.id))
                request.session['notif_count'] = notifications.count()
                notif = Notification.objects.get(pk=id)
                if notif.notif_type.name == 'Role Request Student' or notif.notif_type.name == 'Role Request Adviser':
                    return JsonResponse({'success': True,
                                        'fname': notif.user.first_name,
                                        'mname': notif.user.middle_name,
                                        'lname': notif.user.last_name,
                                        'username': notif.user.username,
                                        'email': notif.user.email,
                                        'course': notif.course,
                                        'date': notif.date_created,
                                        'subject': notif.notif_type.name,
                                        'id': notif.user.id,
                                        'role': notif.user.role.name})
                elif notif.notif_type.name == 'Role Request Approved':
                    if notif.recipient.role.name == 'Student':
                        request = "Role Request Student"
                    elif notif.recipient.role.name == 'Adviser':
                        request = "Role Request Adviser"
                    return JsonResponse({'success': True,
                                        'fname': notif.recipient.first_name,
                                        'mname': notif.recipient.middle_name, 
                                        'lname': notif.recipient.last_name,
                                        'username': notif.recipient.username,
                                        'email': notif.recipient.email,
                                        'date': notif.date_created,
                                        'subject': notif.notif_type.name,
                                        'request': request,
                                        'subject-body':notif.notif_type.name+' by '+notif.user.first_name+notif.user.last_name,
                                        'approved-by': notif.user.first_name+' '+notif.user.last_name})
                elif notif.notif_type.name == 'New Record Proposal/Thesis' or notif.notif_type.name == 'New Record Project' or notif.notif_type.name == 'Resubmission':
                    return JsonResponse({'success': True,
                                        'date': notif.date_created,
                                        'subject': notif.notif_type.name,
                                        'title': notif.record.title,
                                        'classification': notif.record.classification.name,
                                        'psced': notif.record.psced_classification.name,
                                        'recordID': notif.record.id,
                                        'authors': listOfAuthors(request, notif.record.id)})

class RDCONotification(View):
    name = 'notifications/rdco_notification_page.html'
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(Q(to_rdco=True) | Q(recipient=user.id))
        request.session['notif_count'] = notifications.count()
        print(notifications)
        context = {
            'notifications': notifications,
            'category': 'Filter',
        }
        return render(request, self.name, context)
    def post(self, request):
        if request.method == 'POST':
            user = request.user
            # for filter
            if 'all' in request.POST:
                notifications = Notification.objects.filter(Q(to_rdco=True) | Q(recipient=user.id))
                return render(request, self.name, filterHelper(request, notifications, 'ALL'))
            if 'read' in request.POST:
                notifications = Notification.objects.filter((Q(to_rdco=True) | Q(recipient=user.id)) & Q(is_read=True))
                return render(request, self.name, filterHelper(request, notifications, 'Read'))
            if 'unread' in request.POST:
                notifications = Notification.objects.filter((Q(to_rdco=True) | Q(recipient=user.id)) & Q(is_read=False))
                return render(request, self.name, filterHelper(request, notifications, 'Unread'))
            if 'rrs' in request.POST:
                notifications = Notification.objects.filter((Q(to_rdco=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=1)))
                return render(request, self.name, filterHelper(request, notifications, 'Role Request Student'))
            if 'rra' in request.POST:
                notifications = Notification.objects.filter((Q(to_rdco=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=2)))
                return render(request, self.name, filterHelper(request, notifications, 'Role Request Adviser'))
            if 'nrpt' in request.POST:
                notifications = Notification.objects.filter((Q(to_rdco=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=3)))
                return render(request, self.name, filterHelper(request, notifications, 'New Record Proposal/Thesis'))
            if 'nrp' in request.POST:
                notifications = Notification.objects.filter((Q(to_rdco=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=4)))
                return render(request, self.name, filterHelper(request, notifications, 'New Record Project'))
            if 'resubmission' in request.POST:
                notifications = Notification.objects.filter((Q(to_rdco=True) | Q(recipient=user.id)) & Q(notif_type=NotificationType.objects.get(pk=5)))
                return render(request, self.name, filterHelper(request, notifications, 'Resubmissions'))

            if request.POST.get('removeNotification'):
                idList = request.POST.getlist('listOfID[]')
                for id in idList:
                    Notification.objects.get(pk=id).delete()
                return JsonResponse({'success': True})

            if request.POST.get('roleChange'):
                role = request.POST.get('role')
                User.objects.filter(pk=id).update(role=UserRole.objects.get(name=role))
                removeRequest = RoleRequest.objects.get(user=User.objects.get(pk=id))
                removeRequest.delete()
                return JsonResponse({'success': True})

            # content for each notification -> 2nd box content
            if request.POST.get('displayContent'):
                id = request.POST.get('notifID')
                Notification.objects.filter(pk=id).update(is_read=True)
                notifications = Notification.objects.filter(Q(to_rdco=True) | Q(recipient=user.id))
                request.session['notif_count'] = notifications.count()
                notif = Notification.objects.get(pk=id)
                if notif.notif_type.name == 'Role Request Student' or notif.notif_type.name == 'Role Request Adviser':
                    return JsonResponse({'success': True,
                                        'fname': notif.user.first_name,
                                        'mname': notif.user.middle_name,
                                        'lname': notif.user.last_name,
                                        'username': notif.user.username,
                                        'email': notif.user.email,
                                        'course': notif.course,
                                        'date': notif.date_created,
                                        'subject': notif.notif_type.name,
                                        'id': notif.user.id,
                                        'role': notif.user.role.name})
                elif notif.notif_type.name == 'Role Request Approved':
                    if notif.recipient.role.name == 'Student':
                        request = "Role Request Student"
                    elif notif.recipient.role.name == 'Adviser':
                        request = "Role Request Adviser"
                    return JsonResponse({'success': True,
                                        'fname': notif.recipient.first_name,
                                        'mname': notif.recipient.middle_name, 
                                        'lname': notif.recipient.last_name,
                                        'username': notif.recipient.username,
                                        'email': notif.recipient.email,
                                        'date': notif.date_created,
                                        'subject': notif.notif_type.name,
                                        'request': request,
                                        'subject-body':notif.notif_type.name+' by '+notif.user.first_name+notif.user.last_name,
                                        'approved-by': notif.user.first_name+' '+notif.user.last_name})
                elif notif.notif_type.name == 'New Record Proposal/Thesis' or notif.notif_type.name == 'New Record Project' or notif.notif_type.name == 'Resubmission':
                    return JsonResponse({'success': True,
                                        'date': notif.date_created,
                                        'subject': notif.notif_type.name,
                                        'title': notif.record.title,
                                        'classification': notif.record.classification.name,
                                        'psced': notif.record.psced_classification.name,
                                        'recordID': notif.record.id,
                                        'authors': listOfAuthors(request, notif.record.id)})


class TBINotification(View):
    name = 'notifications/index.html'
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(Q(to_ktto=True) | Q(recipient=user.id))
        request.session['notif_count'] = notifications.count()
        print(notifications)
        context = {
            'notifications': notifications,
        } 
        return render(request, self.name, context)
    def post(self, request):
        if request.method == 'POST':
            user = request.user
            id = request.POST.get('notifID')
            Notification.objects.filter(pk=id).update(is_read=True)
            notifications = Notification.objects.filter(Q(to_ktto=True) | Q(recipient=user.id))
            request.session['notif_count'] = notifications.count()
            notif = Notification.objects.get(pk=id)
            return JsonResponse({'success': True,
                                'fname': notif.user.first_name,
                                'mname': notif.user.middle_name,
                                'lname': notif.user.last_name,
                                'username': notif.user.username,
                                'email': notif.user.email,
                                'course': notif.course,
                                'date': notif.date_created,
                                'subject': notif.notif_type.name})

class ITSONotification(View):
    name = 'notifications/index.html'
    def get(self, request):
        return render(request, self.name)

# class NotificationsHomeView(View):
#     name = 'notifications/index.html'

#     def get(self, request):
#         user = request.user
#         received_notifications = Notification.objects.filter(recipient=user)
#         context = {
#             'received_notifications': received_notifications,
#         }
#         return render(request, self.name, context)
