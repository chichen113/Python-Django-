from django.urls import path
from . import views
from .views import upload_csv


urlpatterns = [
    path('test', views.test),
    path('run', views.run),
    path('run-explain', views.run_explain),
    path('upload-csv', upload_csv, name='upload_csv'),
    path('list-question', views.list_question),
    path('add-question', views.add_question),
    path('modify-question', views.modify_question),
    path('del-question', views.del_question),
    path('list-set', views.list_set),
]