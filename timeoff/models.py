from django.db import models
from user_management.models import *
# Create your models here.
class TimeoffType(models.Model):
    name=models.TextField(null=True)
    limit=models.IntegerField(null=True)
    status=models.IntegerField(null=True)
    class Meta:
        db_table = "timeoff_type"


class TimeoffHeader(models.Model):
    time_off_type=models.ForeignKey(TimeoffType, on_delete=models.CASCADE,related_name="TimeoffHeader_timeoff_type", null=True)
    subject=models.TextField(null=True)
    description=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "timeoff_header"

class TimeoffHeaderDateMapping(models.Model):
    timeoff_header=models.ForeignKey(TimeoffHeader, on_delete=models.CASCADE,related_name="TimeoffHeaderDateMapping_timeoff_header", null=True)
    date=models.DateField(null=True)
    class Meta:
        db_table = "timeoffheader_date_mapping"