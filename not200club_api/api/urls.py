from django.urls import path
from .views import ping, dispatch_task, check_task

urlpatterns = [
    path('ping', ping, name="ping"),
    path('dispatch-task', dispatch_task, name='dispatch-task'),
    path('check-task/<str:id>', check_task, name="check-task"),
]
