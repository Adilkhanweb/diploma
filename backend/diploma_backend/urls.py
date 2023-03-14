from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from diploma_backend.views import DashboardView

app_name = "core"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('quiz/', include('quiz_apps.quiz.urls')),
    path("", include("calendarapp.urls")),
    path("problems/", include("problems.urls")),
    path("assignments/", include("assignment.urls")),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'account.views.page_not_found'