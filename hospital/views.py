from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import *
from hospital.random_generator import *
from datetime import datetime, timedelta, date
from django import template

register = template.Library()


@register.filter()
def addDays(days):
    newDate = datetime.today() + timedelta(days=days)
    return newDate


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        type = request.POST['Type']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.last_name == "Employee":
                if int(type) == 0:
                    auth.login(request, user)
                    return redirect("/")
                else:
                    messages.info(request, "Wrong Type!")
                    return redirect('login')
            else:
                if int(type) == 1:
                    auth.login(request, user)
                    return redirect("/")
                else:
                    messages.info(request, "Wrong Type!")
                    return redirect('login')
        else:
            messages.info(request, "Password or Username invalid!")
            return redirect('login')
    else:
        return render(request, 'Login.html')


def register(request):
    if (request.method == 'POST'):
        employee_id = request.POST['empid']
        email = request.POST['emailid']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=employee_id).exists():
                messages.info(request, 'Employee already registered')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('register')
            if len(Employee.objects.filter(empid=employee_id, empmail=email)) == 0:
                messages.info(request, 'Employee not found')
                return redirect('register')
            user = User.objects.create_user(username=employee_id, password=password1, email=email, )
            user.last_name = "Employee"
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your hospital account.'
            message = render_to_string('acc_active_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, "Accept your email confirmation")
            return redirect('register')
        else:
            messages.info(request, "Password doesn't match")
            return redirect('register')


    else:
        return render(request, 'Register1.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


DAY_CHOICES = [
    'MON',
    'TUES',
    'WED',
    'THURS',
    'FRI',
    'SAT',
    'SUN'
]
DAY_CHOICES2 = [
    'MONDAY',
    'TUESDAY',
    'WEDNESDAY',
    'THURSDAY',
    'FRIDAY',
    'SATURDAY',
    'SUNDAY'
]

DateHelp = {
    "January": "1",
    "February": "2",
    "March": "3",
    "April": "4",
    "May": "5",
    "June": "6",
    "July": "7",
    "August": "8",
    "September": "9",
    "October": "10",
    "November": "11",
    "December": "12"
}

dept = None
days = 0


def calculate_time(shift, slot):
    if shift == 1:
        time = datetime(100, 1, 1, 8, 0, 0) + timedelta(0, 60 * slot * 15)
        return time.time()
    if shift == 2:
        time = datetime(100, 1, 1, 13, 0, 0) + timedelta(0, 60 * slot * 15)
        return time.time()
    if shift == 3:
        time = datetime(100, 1, 1, 18, 0, 0) + timedelta(0, 60 * slot * 15)
        return time.time()


def book_appoint(request):
    DateList1 = [(datetime.today() + timedelta(days=0)).date(), ]
    DateList2 = [(datetime.today() + timedelta(days=1)).date(), ]
    DateList3 = [(datetime.today() + timedelta(days=2)).date(), ]
    DateList4 = [(datetime.today() + timedelta(days=3)).date(), ]
    DateList5 = [(datetime.today() + timedelta(days=4)).date(), ]
    DateList6 = [(datetime.today() + timedelta(days=5)).date(), ]
    DateList7 = [(datetime.today() + timedelta(days=6)).date(), ]
    global days, dept
    dayx = addDays(days)
    dayx = DAY_CHOICES[dayx.weekday()]
    if dept is not None:
        query = Schedule.objects.filter(doc__dept__deptid=int(dept) + 1, day=dayx)
    else:
        query = Schedule.objects.filter(day=dayx)
    context = {}
    if (request.user.is_authenticated):
        val = request.user.username
        q2 = Employee.objects.filter(empid=int(val))
        query2 = Dependent.objects.filter(empl__empid=int(val))
        context = {'query': query, 'query2': query2, 'DateList1': DateList1, 'DateList2': DateList2,
                   'DateList3': DateList3, 'DateList4': DateList4, 'DateList5': DateList5, 'DateList6': DateList6,
                   'DateList7': DateList7}
    if request.method == 'POST':
        if 'filter' in request.POST:
            dept = request.POST['filter']
            query = Schedule.objects.filter(doc__dept__deptid=int(dept) + 1, day=dayx)
            val = request.user.username
            q2 = Employee.objects.filter(empid=int(val))
            query2 = Dependent.objects.filter(empl=q2[0])
            context = {'query': query, 'query2': query2, 'DateList1': DateList1, 'DateList2': DateList2,
                       'DateList3': DateList3, 'DateList4': DateList4, 'DateList5': DateList5, 'DateList6': DateList6,
                       'DateList7': DateList7}
            return render(request, 'Book_appoint.html', context)

        elif 'docId' in request.POST:
            DateList = []
            for i in range(7):
                DateList.append(datetime.today() + timedelta(days=i))
            dep_id = request.POST['patient']
            adateindex = request.POST['date']
            adate = datetime.today() + timedelta(days=int(adateindex) - 1)
            shift = int(request.POST['time']) + 1
            docId = int(request.POST['docId'])
            doctor = Doctor.objects.filter(docid=int(docId))[0]
            isUpgradable = ('upgrade' in request.POST)
            empl = request.user.username
            dep = Dependent.objects.filter(depid=int(dep_id))[0]
            emp = Employee.objects.filter(empid=int(empl))[0]
            patient_id = empl + "D" + dep_id
            sched = Schedule.objects.filter(doc__docid=docId, day=DAY_CHOICES[int(adate.weekday())])
            print("reached")
            print(len(sched))
            if len(sched) == 0:
                messages.info(request, "Doctor not availaible for this date")
                return render(request, 'Book_appoint.html', context)
            if shift == 1 and sched.filter(shift1=True) is None:
                messages.info(request, "Doctor not availaible for shift 1")
                print("Doctor not availaible for shift 1")
                return render(request, 'Book_appoint.html', context)
            elif shift == 2 and sched.filter(shift2=True) is None:
                messages.info(request, "Doctor not availaible for shift 2")
                print("Doctor not availaible for shift 2")
                return render(request, 'Book_appoint.html', context)
            elif shift == 3 and sched.filter(shift3=True) is None:
                messages.info(request, "Doctor not availaible for shift 3")
                print("Doctor not availaible for shift 3")
                return render(request, 'Book_appoint.html', context)
            if len(Leave.objects.filter(doc__docid=docId, date=adate, Shift=shift-1)) > 0:
                messages.info(request, "Doctor not availaible for shift 3")
                print("Doctor not availaible for shift" + str(shift))
                return render(request, 'Book_appoint.html', context)
            appoinments = Appointments.objects.filter(doc__docid=docId, adate=adate, shift=shift)
            if len(Appointments.objects.filter(pat_id=patient_id, sched=sched[0], adate=adate)) != 0:
                messages.info(request, "You have already booked this slot for this patient")
                print("You have already booked this slot for this patient")
                return render(request, 'Book_appoint.html', context)
            if len(appoinments) >= 12:
                messages.info(request, "All slots of doctor is full")
                return render(request, 'Book_appoint.html', context)
            time = str(calculate_time(shift, len(appoinments)))
            appt = Appointments.objects.create(time=time, empl=emp, patient=dep, doc=doctor, pat_id=patient_id,
                                              sched=sched[0], adate=adate, shift=shift, IsUpgradable=isUpgradable,
                                              slot=(len(appoinments) + 1))
            appt.save()

            return render(request, 'view_appoint.html', context)
        else:
            return render(request, 'Book_appoint.html', context)
    else:
        return render(request, 'Book_appoint.html', context)


def view_appoint(request):
    empid = int(request.user.username)
    query = Appointments.objects.filter(empl__empid=empid)
    query1 = Appointments.objects.filter(empl__empid=empid).distinct('doc__docid')
    query2 = Dependent.objects.filter(empl__empid=int(request.user.username))
    context = {'query': query, 'query1': query1, 'query2': query2}
    if request.method == 'POST':
        if 'docId' in request.POST:
            docid = int(request.POST['docId'])
            date1 = request.POST['appoint_date']
            year, month, day = map(int, date1.split('-'))
            date1 = date(year, month, day)
            shift = int(request.POST['time']) + 1
            depid = int(request.POST['patient'])
            query4 = Appointments.objects.filter(doc__docid=docid, adate=date1, shift=shift, patient__depid=depid)
            Appointments.objects.filter(doc__docid=docid, adate=date1, shift=shift, patient__depid=depid).delete()
            query = Leave.objects.filter(date__gt=date.today())
            query1 = Doctor.objects.all()
            query2 = Dependent.objects.filter(empl__empid=int(request.user.username))
            context = {'query': query, 'query1': query1, 'query2': query2}
            return render(request, 'view_appoint.html', context)
    return render(request, 'view_appoint.html', context)

def mail(query):
    for i in query.values('empl__empmail', 'doc__docname', 'adate', 'time'):
        email = i['empl__empmail']
        mail_subject = 'Cancellation of Appointment'
        message = "Dear patient,\nYour appointment with " + i['doc__docname'] + " on " + str(i['adate']) + " between " + str(i['time']) +" has been cancelled due to unavailibility of the doctor. Please re-book ypur appointment"
        print(message)
        to_email = email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
    print("reached")


def send_mail(query):
    for i in query.values('empl__empmail', 'doc__docname', 'adate', 'time'):
        email = i['empl__empmail']
        mail_subject = 'Cancellation of Appointment'
        message = "Dear patient,\nYour appointment with " + i['doc__docname'] + " on " + str(
            i['adate']) + " between " + str(
            i['time']) + " has been changed due to unavailibility of the doctor. Please look into your account for new Timings."
        print(message)
        to_email = email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
    print("reached")

def apply_leave(request):
    docid = int(request.user.username.strip("doc"))
    query = Schedule.objects.filter(doc__docid=docid)
    context = {'query': query}
    if request.method == 'POST':
        if 'Shift' in request.POST:
            date1 = request.POST['leave_date']
            shift= request.POST['Shift']
            docid= int(request.user.username.strip("doc"))
            doc = Doctor.objects.filter(docid=docid)[0]
            year, month, day = map(int, date1.split('-'))
            date1 = date(year, month, day)
            print(date1.weekday())
            if len(Leave.objects.filter(doc=doc, date=date1, Shift=int(shift))) !=0 :
                print("Already taken leave")
                messages.info(request, "Already taken leave")
                return redirect('apply_leave')
            if len(Schedule.objects.filter(doc__docid=docid, day=DAY_CHOICES[date1.weekday()])) == 0:
                print("No schedule on this shift")
                messages.info(request, "No schedule on this shift")
                return redirect('apply_leave')
            leaveobj = Leave.objects.create(doc=doc, date=date1, Shift=shift)
            leaveobj.save()
            query1 = Appointments.objects.filter(sched__doc__docid=docid,sched__day=DAY_CHOICES[date1.weekday()], shift=int(shift)+1, IsUpgradable=False)
            mail(query1)
            Appointments.objects.filter(sched__doc__docid=docid,sched__day=DAY_CHOICES[date1.weekday()], shift=int(shift)+1, IsUpgradable=False).delete()
            query2 = Appointments.objects.filter(sched__doc__docid=docid,sched__day=DAY_CHOICES[date1.weekday()], shift=int(shift)+1, IsUpgradable=True)
            first_pointer = (date1.weekday()+1) %7
            print(len(query2))
            for i in range(6):
                query3 = Schedule.objects.filter(doc__docid=docid, day=DAY_CHOICES[first_pointer])[0]
                s1 = getattr(query3, 'shift1')
                s2 = getattr(query3, 'shift2')
                s3 = getattr(query3, 'shift3')
                date2 = date1 + timedelta(days=i+1)
                query4 = Appointments.objects.filter(doc__docid=docid, shift=1, sched__day=DAY_CHOICES[first_pointer], IsUpgradable=True)
                query5 = Appointments.objects.filter(doc__docid=docid, shift=2, sched__day=DAY_CHOICES[first_pointer],
                                                     IsUpgradable=True)
                query6 = Appointments.objects.filter(doc__docid=docid, shift=3, sched__day=DAY_CHOICES[first_pointer],
                                                     IsUpgradable=True)
                send_mail(query2)
                if s1 == True and len(query4) + len(query2) <= 12:
                    for i in query2.values('patient', 'pat_id', 'doc', 'empl'):
                        slot = len(query4)
                        dep = Dependent.objects.filter(depid=i['patient'])[0]
                        empl = Employee.objects.filter(empid=i['empl'])[0]

                        appt = Appointments.objects.create(adate=date2,sched=query3, patient=dep, pat_id=i['pat_id'], shift=1, doc=doc,empl=empl,IsUpgradable=True, slot=slot+1, time=str(calculate_time(1, slot)))
                        appt.save()
                    break
                elif s2 == True and len(query5) + len(query2) <= 12:
                    for i in query2.values('patient', 'pat_id', 'doc', 'empl'):
                        slot = len(query5)
                        dep = Dependent.objects.filter(depid=i['patient'])[0]
                        empl = Employee.objects.filter(empid=i['empl'])[0]
                        appt = Appointments.objects.create(adate=date2,sched=query3, patient=dep, pat_id=i['pat_id'], shift=2, doc=doc, empl=empl,IsUpgradable=True, slot=slot+1, time= str(calculate_time(2, slot)))
                        appt.save()
                    break
                elif s3 == True and len(query6) + len(query2) <= 12:
                    for i in query2.values('patient', 'pat_id', 'doc', 'empl'):
                        slot = len(query6)
                        dep = Dependent.objects.filter(depid=i['patient'])[0]
                        empl = Employee.objects.filter(empid=i['empl'])[0]

                        appt = Appointments.objects.create(adate=date2, sched=query3, patient=dep,
                                                           pat_id=i['pat_id'], shift=3, doc=doc, empl=empl,
                                                           IsUpgradable=True, slot=slot + 1,
                                                           time= str(calculate_time(3, slot)))
                        appt.save()
                        break
                first_pointer = (first_pointer+1)%7
            Appointments.objects.filter(sched__doc__docid=docid, sched__day=DAY_CHOICES[date1.weekday()],
                                        shift=int(shift) + 1).delete()
            return render(request, 'apply_leave.html', context)
    return render(request, 'apply_leave.html', context)

def filter_d2(request):
    global days
    days = 1
    return book_appoint(request)


def filter_d3(request):
    global days
    days = 2
    return book_appoint(request)


def filter_d4(request):
    global days
    days = 3
    return book_appoint(request)


def filter_d5(request):
    global days
    days = 4
    return book_appoint(request)


def filter_d6(request):
    global days
    days = 5
    return book_appoint(request)


def filter_d7(request):
    global days
    days = 6
    return book_appoint(request)


def view_leave(request):
    query = Leave.objects.filter(date__gt=date.today())
    context = {'query', query}
    return render(request, 'view_leave.html', context)
