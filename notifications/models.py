from django.db import models
from accounts.models import User
from records.models import Record
from ckeditor.fields import RichTextField

# Role Request Student, Role Request Adviser, New Record Proposal/Thesis, New Record Project, Resubmission, Role Request Status [advisers, ktto, rdco, tbi]
# Comments, Record Approved, Record Decline [students, advisers, ktto, rdco, tbi]
class NotificationType(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='user')
    record = models.ForeignKey(Record, on_delete=models.CASCADE, blank=True, null=True, related_name='record')
    notif_type = models.ForeignKey(NotificationType, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='notif_type')
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)