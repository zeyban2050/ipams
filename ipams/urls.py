from django.contrib import admin
from django.urls import path, include
import social.apps.django_app.urls as social_urls

urlpatterns = [
    path('', include('records.urls')),
    path('account/', include('accounts.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),

    path('social/', include(social_urls, namespace='social')),
]
