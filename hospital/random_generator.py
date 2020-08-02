import random
from .models import *
import string
import datetime


def doctors():
    query1 = Doctor.objects.all()
    query2 = Department.objects.all()
    print(query2, query1)
    l = [i for i in range(1, 100)]
    for i in query1:
        l.remove(i.docid)
    docid = random.choice(l)
    docname = ''.join(random.choices(string.ascii_uppercase, k=8))
    dept_no = random.choice([i for i in range(0, len(query2))])
    dept = query2[dept_no]
    fee = random.randrange(300, 500, 3)
    doc = Doctor.objects.create(docid=docid, docname=docname, dept=dept, fee=fee)
    doc.save()


def employee():
    EMP_TYPE = ['RET', 'EXEC', 'NEXEC']
    query1 = Employee.objects.all()
    l = [i for i in range(1, 1000)]
    for i in query1:
        l.remove(i.empid)
    empid = random.choice(l)
    emname = ''.join(random.choices(string.ascii_uppercase, k=8))
    emmail = ''.join(random.choices(string.ascii_uppercase, k=8)) + "@gmail.com"
    etype = EMP_TYPE[random.choice([0, 1, 2])]
    edob = datetime.date(random.randrange(1930, 2005, 3), random.randrange(1, 12, 3), random.randrange(1, 28, 3))
    gender = random.choice(['M', 'F'])
    fine = 0
    finedate = datetime.date(2100, 12, 31)
    EMP = Employee.objects.create(empid=empid, empname=emname, empmail=emmail, etype=etype, edob=edob, gender=gender,
                                  fine=fine, finedate=finedate)
    EMP.save()


def depenedent():
    query1 = Dependent.objects.all()
    query2 = Employee.objects.all()
    l = [i for i in range(0, 2000)]
    for i in query1:
        l.remove(i.depid)
    depid = random.choice(l)
    depname = ''.join(random.choices(string.ascii_uppercase, k=8))
    depdob = datetime.date(random.randrange(1930, 2005, 3), random.randrange(1, 12, 3), random.randrange(1, 28, 3))
    depgender = random.choice(['M', 'F'])
    empl = query2[random.choice([i for i in range(len(query2))])]
    print(empl)
    DEP = Dependent.objects.create(depid=depid, depdob=depdob, depname=depname, depgender=depgender, empl=empl)
    DEP.save()


DAY_CHOICES = [
    'MON',
    'TUES',
    'WED',
    'THURS',
    'FRI',
    'SAT',
    'SUN'
]


def schedule():
    day = random.choice(DAY_CHOICES)
    shift1 = random.choice([0, 1])
    shift2 = random.choice([0, 1])
    shift3 = random.choice([0, 1])
    query = Doctor.objects.all()
    doc = query[random.choice([i for i in range(len(query))])]
    query2 = Schedule.objects.filter(doc=doc, day=day)
    print(query2)
    if len(query2) == 0:
        SCH = Schedule.objects.create(day=day, shift1=shift1, shift2=shift2, shift3=shift3, doc=doc)
        SCH.save()
