from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('', include('records.urls')),
    path('account/', include('accounts.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
