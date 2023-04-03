from django.urls import path

from discussions import views

# Create your models here.
app_name = 'discussions'
urlpatterns = [
    path('', views.index, name='discussions-list'),
]
