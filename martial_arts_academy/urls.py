from django.contrib import admin
from django.urls import include, path
from martial_arts_academy.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('martial-arts/', include('martial_arts.urls')),
    path('events/', include('events.urls')),
    path('curriculum/', include('curriculum.urls')),
    path('accounts/', include('accounts.urls')),
    path('training/', include('training.urls')),
]
