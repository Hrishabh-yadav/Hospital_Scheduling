from django.db import models

# Create your models here.
GENDER_CHOICES = [
    ('F', 'female'),
    ('M', 'male'),
]
DAY_CHOICES = [
    ('SUN', 'sunday'),
    ('MON', 'monday'),
    ('TUES', 'tuesday'),
    ('WED', 'wednesday'),
    ('THURS', 'thursday'),
    ('FRI', 'friday'),
    ('SAT', 'saturday'),
]


class Department(models.Model):
    deptid = models.IntegerField(primary_key=True)
    deptname = models.CharField(max_length=20)


class Doctor(models.Model):
    docid = models.IntegerField(primary_key=True)
    docname = models.CharField(max_length=30)
    dept = models.ForeignKey("Department", on_delete=models.CASCADE)
    fee = models.IntegerField()


class Schedule(models.Model):
    day = models.CharField(max_length=5, choices=DAY_CHOICES)
    shift1 = models.BooleanField();
    shift2 = models.BooleanField();
    shift3 = models.BooleanField();
    doc = models.ForeignKey("Doctor", on_delete=models.CASCADE)




class Employee(models.Model):
    EMP_TYPE_CHOCES = [
        ('RET', 'retired'),
        ('EXEC', 'executive'),
        ('NEXEC', 'non-executive'),
    ]
    empid = models.IntegerField(primary_key=True)
    empname = models.CharField(max_length=30)
    empmail = models.EmailField(max_length=254, default="no_email@gmail.com")
    etype = models.CharField(max_length=5, choices=EMP_TYPE_CHOCES, default='EXEC')
    edob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    fine = models.BooleanField(default=0)
    finedate = models.DateField()


class Dependent(models.Model):
    depid = models.IntegerField(primary_key=True)
    depname = models.CharField(max_length=30)
    depdob = models.DateField()
    depgender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    empl = models.ForeignKey("Employee", on_delete=models.CASCADE)


class Appointments(models.Model):
    adate = models.DateField()
    sched = models.ForeignKey("Schedule", on_delete=models.CASCADE)
    patient = models.ForeignKey("Dependent", on_delete=models.CASCADE)
    pat_id = models.CharField(max_length=60)
    shift = models.IntegerField()
    doc = models.ForeignKey("Doctor", on_delete=models.CASCADE)
    empl = models.ForeignKey("Employee", on_delete=models.CASCADE)
    IsUpgradable = models.BooleanField(default=1)
    slot = models.IntegerField(default=0)
    time = models.CharField(max_length=30)


class Leave(models.Model):
    doc = models.ForeignKey("Doctor", on_delete=models.CASCADE)
    date = models.DateField()
    Shift = models.IntegerField(default = 1)