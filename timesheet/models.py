from django.db import models
from user_management.models import *
# Create your models here.

class TimeSheetHeader(models.Model):
    task=models.TextField(null=True)
    task_date=models.DateField(null=True)
    description=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "timesheet_header"
