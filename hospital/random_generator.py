import random
from .models import *
import string
import datetime

def doctors():
    query1 = Doctor.objects.all()
    query2 = Department.objects.all()
    l = [i for i in range(1, 100)]
    print(l)
    for i in query1:
        l.remove(i.docid)
    docid = random.choice(l)
    docname = ''.join(random.choices(string.ascii_uppercase , k = 8))
    dept_no = random.choice([i for i  in range(0, len(query2)) ] )
    dept = query2[dept_no]
    fee  = random.randrange(300, 500, 3)
    doc = Doctor.objects.create(docid=docid, docname=docname,dept=dept,fee=fee)
    doc.save()

def employee():
    EMP_TYPE = ['RET' , 'EXEC','NEXEC' ]
    query1 = Employee.objects.all()
    l = [i for i in range(1, 1000)]
    print(l)
    for i in query1:
        l.remove(i.empid)
    empid = random.choice(l)
    emname = ''.join(random.choices(string.ascii_uppercase, k=8))
    emmail = ''.join(random.choices(string.ascii_uppercase, k=8)) + "@gmail.com"
    etype = EMP_TYPE[random.choice([0,1,2])]
    edob = datetime.date(random.randrange(1930, 2005, 3),random.randrange(1, 12, 3),random.randrange(1, 28, 3))
    gender = random.choice(['M', 'F'])
    fine = 0
    finedate = datetime.date(2100, 12, 31)
    EMP = Employee.objects.create(empid=empid, emname=emname,emmail=emmail, etype=etype, edob=edob, gender=gender, fine=fine, finedate=finedate)
    EMP.save()