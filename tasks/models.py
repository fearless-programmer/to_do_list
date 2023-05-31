from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Plan(models.Model):
    user = models.ForeignKey(User, related_name='tasks_plans', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title
    

class Task(models.Model):
    # id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField(default=None)
    end_date = models.DateField()
    end_time = models.TimeField(default=None)
    reminder = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)
    forgotten = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date', 'start_time']

    def __str__(self):
        return self.title
    def start_year(self):
        return self.start_date.strftime('%Y')
    def start_month(self):
        return int(self.start_date.strftime('%m'))-1
    def start_day(self):
        return self.start_date.strftime('%d') 