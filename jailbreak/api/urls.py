from django.urls import path
from . import views
from .views import upload_csv
from .views import upload_json


urlpatterns = [
    path('test', views.test),
    path('run', views.run),
    path('run-explain', views.run_explain),
    path('upload-csv', upload_csv, name='upload_csv'),
    path('upload-json', upload_json),
    path('list-question', views.list_question),
    path('add-question', views.add_question),
    path('modify-question', views.modify_question),
    path('del-question', views.del_question),
    path('list-set', views.list_set),
    path("TestSuiteCreate", views.test_suit_create),
    path("TestSuiteShow", views.test_suit_show),
    path("TestCreate", views.test_create),
    path("TestShow", views.test_show),
    path("config", views.config),
    path("TaskCreate", views.task_create),
    path("TaskShow", views.task_show),
    path("TaskInfo", views.task_info),
    path("TaskExec", views.task_exec),
    path("TaskResult", views.task_res),
    path("TestSuiteDele", views.test_suite_dele),
    path("TestDele", views.test_dele),
    path("TaskDele", views.task_dele)
]