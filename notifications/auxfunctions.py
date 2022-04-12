from accounts.models import UserRecord

# filter notifications
def filterHelper(request, notifications, category):
    request.session['notif_count'] = notifications.count()
    print(notifications)
    context = {
        'notifications': notifications,
        'category': category,
    }
    return context

def listOfAuthors(request, recordID):
    authors = []
    record_authors = UserRecord.objects.filter(record=recordID)
    for author in record_authors:
        authors.append(author.user.first_name+' '+author.user.last_name+', ')
    return authors