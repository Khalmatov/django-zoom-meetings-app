from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from .views import *

from django.conf.urls.static import static
import debug_toolbar

from django.views.generic.base import RedirectView


urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('admin/', admin.site.urls),
	path('accounts/', include('django.contrib.auth.urls')),
	path('meetings/', MeetingListView.as_view(), name='meetings'),
	re_path(r'^meeting/(?P<uuid>.+)/$', MeetingDetailView.as_view(), name='meeting'),
	path('participants/', ParticipantListView.as_view(), name='participants'),
	path('participant/<int:id>/', ParticipantDetailView.as_view(), name='participant'),
	path('courses/2/', SecondCourseView.as_view(), name='secondcourse'),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)