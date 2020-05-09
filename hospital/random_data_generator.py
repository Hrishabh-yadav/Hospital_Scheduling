import random
from .models import *
import string
def doctors():
    query1 = Doctor.objects.all()
    query2 = Department.objects.all()
    l = [i for i in range(1, 100)]
    for i in query1:
        l.remove(i.docid)
    docid = random.choice(l)
    docname = ''.join(random.choices(string.ascii_uppercase , k = 8))
    dept_no = random.choice([i for i  in range(0, len(query2)) ] )
    dept = query2[dept_no]
    fee  = random.randrange(300, 500, 3)
    doc = Doctor.objects.create_user(docid=docid, docname=docname,dept=dept,fee=fee)
    doc.save()