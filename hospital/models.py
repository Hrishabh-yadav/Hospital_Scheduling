from django.db import models

# Create your models here.
class Doctor(models.Model):
    docid = models.IntegerField()
    docname = models.CharField(max_length=50)
    deptno = models.IntegerField()
    deptname = models.CharField(max_length=15)
    passwd = models.CharField(max_length=50)
    fees = models.IntegerField()
    isdoc = models.BooleanField(default=True)