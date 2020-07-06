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
from datetime import datetime, timedelta
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
DAY_CHOICES2= [
    'MONDAY',
    'TUESDAY',
    'WEDNESDAY',
    'THURSDAY',
    'FRIDAY',
    'SATURDAY',
    'SUNDAY'
]


DateHelp = {
    "January" : "1",
    "February" : "2",
    "March" : "3",
    "April" : "4",
    "May" : "5",
    "June" : "6",
    "July" : "7",
    "August" : "8",
    "September" : "9",
    "October" : "10",
    "November" : "11",
    "December" : "12"
}

dept = None
days = 0
def book_appoint(request):
    #day1 = DAY_CHOICES[datetime.datetime.today().weekday()]

    DateList1 = [(datetime.today() + timedelta(days=0)).date(), ];
    DateList2 = [(datetime.today() + timedelta(days=1)).date(), ];
    DateList3 = [(datetime.today() + timedelta(days=2)).date(), ];
    DateList4 = [(datetime.today() + timedelta(days=3)).date(), ];
    DateList5 = [(datetime.today() + timedelta(days=4)).date(), ];
    DateList6 = [(datetime.today() + timedelta(days=5)).date(), ];
    DateList7 = [(datetime.today() + timedelta(days=6)).date(), ];

    specialMessage = [];
    global days, dept
    dayx = addDays(days)
    dayx = DAY_CHOICES[dayx.weekday()]
    if dept is not None:
        query = Schedule.objects.filter(doc__dept__deptid=int(dept) + 1, day=dayx)
    else:
        query = Schedule.objects.filter(day=dayx)
    context = {}
    if(request.user.is_authenticated):
        val = request.user.username
        q2 = Employee.objects.filter(empid=int(val))
        query2 = Dependent.objects.filter(empl=q2[0])
        context = {'query': query, 'query2': query2,'DateList1': DateList1, 'DateList2': DateList2, 'DateList3': DateList3,'DateList4': DateList4, 'DateList5': DateList5, 'DateList6': DateList6, 'DateList7': DateList7}
    if request.method == 'POST':
        if 'filter' in request.POST:
            dept = request.POST['filter']
            query = Schedule.objects.filter(doc__dept__deptid=int(dept) + 1, day=dayx)
            val = request.user.username
            q2 = Employee.objects.filter(empid = int(val))
            query2 = Dependent.objects.filter(empl = int(q2[0]))
            context = {'query': query, 'query2': query2, 'DateList1': DateList1, 'DateList2': DateList2, 'DateList3': DateList3,'DateList4': DateList4, 'DateList5': DateList5, 'DateList6': DateList6, 'DateList7': DateList7}
            return render(request, 'Book_appoint.html', context)

        elif 'docId' in request.POST:
            #print(request.POST)
            DateList = [];
            for i in range(7):
                DateList.append(datetime.today() + timedelta(days=i))

            patient = request.POST['patient']

            adateindex = request.POST['date']
            adate = datetime.today() + timedelta(days=int(adateindex) - 1)

            shift = int(request.POST['time']) + 1
            print("shift ", shift)
            docId = request.POST['docId']
            doctor = Doctor.objects.filter(docid=docId)

            isUpgradable = request.POST['upgrade']

            empl = request.user.username

            patient_id = ""
            dep = Dependent.objects.filter(empl=empl)

            for item in dep:
                patient_id = empl + "D" + str(item.depid)

            sched = Schedule.objects.filter(doc__docid=docId, day=DAY_CHOICES[adate.weekday()])
            if(len(sched) == 0):
                messages.info(request, "Doctor not availaible for this date")
                return redirect('book_appoint')
            for i in sched.values():
                print(i)
            #print(sched.filter(shift1=True) is None);
            if shift == 1 and sched.filter(shift1=True) is None:
                messages.info(request, "Doctor not availaible for shift 1")
                return redirect('book_appoint')
            elif shift == 2 and sched.filter(shift2=True) is None:
                messages.info(request, "Doctor not availaible for shift 2")
                return redirect('book_appoint')
            elif shift == 3 and sched.filter(shift3=True) is None:
                messages.info(request, "Doctor not availaible for shift 3")
                return redirect('book_appoint')

            if (Appointment.objects.filter(p_id=patient_id, sched=sched[0], adate=adate)) is not None:
                messages.info(request, "You have already booked this slot for this patient")
                return redirect('book_appoint')
            
            appt = Appointment.objects.create(p_id=patient_id, sched=sched[0], adate=adate, shift=shift)



            #print(appt.adate, appt.p_id, appt.sched, appt.shift)
            appt.save()

            return render(request, 'view_appoint.html')
        else:
            return render(request, 'Book_appoint.html', context)
    else:
        return render(request, 'Book_appoint.html', context)


def filter_d2(request):
    global days
    days = 1
    return book_appoint(request)

def filter_d3(request):
    global days
    days =2
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
    days=6
    return book_appoint(request)

def view_appoint(request):
    return render(request, 'view_appoint.html')

def apply_leave(request):
    return render(request, 'apply_leave.html')

def view_leave(request):
    return render(request, 'view_leave.html')

