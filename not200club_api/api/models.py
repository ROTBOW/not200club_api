from django.db import models
from datetime import timedelta

# Create your models here.
class Task(models.Model):
    task_id = models.CharField(max_length=255, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    task_finished = models.BooleanField(default=False)
    
    status_code = models.CharField(max_length=255, default='418')
    bad_url = models.BooleanField(default=False)
    time_to_respond = models.DurationField(default=timedelta(seconds=600))
    timeout_res = models.BooleanField(default=False)
    no_link = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return (self.task_id, self.task_finished)
    
class TaskThread(models.Model):
    thread_id = models.CharField(max_length=255, default='')
    
    def __str__(self) -> str:
        return self.thread_id