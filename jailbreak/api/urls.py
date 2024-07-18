from django.urls import path
from . import views
from .views import upload_csv


urlpatterns = [
    path('test', views.test),
    path('run', views.run),
    path('run-explain', views.run_explain),
    path('upload-csv', upload_csv, name='upload_csv'),
    path('r1', views.r1),
]