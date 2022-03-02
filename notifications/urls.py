from django.urls import path
from . import views
from records import views as record_views

urlpatterns = [
    path('', views.NotificationsHomeView.as_view(), name='notifications-home'),
]
