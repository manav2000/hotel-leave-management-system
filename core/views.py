from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import student_required, teacher_required, warden_required
from leave_system.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.contrib import messages
from .filters import LeaveFilter
from .models import *
from .forms import *

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

# Create your views here.


def index(request):
    return render(request, 'main/index.html', {})


@login_required
@teacher_required
def teacher_view(request):
    applications = Applications.objects.filter(
        mentor=Mentor.objects.get(user=request.user))
    return render(request, 'main/teacher_view.html', {
        'applications': applications
    })


@login_required
@student_required
def student_view(request):
    requests = Applications.objects.filter(
        student=Student.objects.get(user=request.user))
    return render(request, 'main/student_view.html', {
        'requests': requests
    })


def student_sign_up_view(request, *args, **kwargs):
    user_form = StudentSignUpForm(request.POST or None)

    if user_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.is_student = True
        user.save()
        messages.success(request, 'You are successfully created an account, Now login to continue')
        return redirect('index')

    context = {
        'user_form': user_form,
    }
    return render(request, "main/student_register.html", context)


def teacher_sign_up_view(request, *args, **kwargs):
    user_form = TeacherSignupForm(request.POST or None)

    if user_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.is_mentor = True
        user.save()
        messages.success(request, 'You are successfully created an account, Now login to continue')
        return redirect('index')

    context = {
        'user_form': user_form,
    }
    return render(request, "main/techer_register.html", context)

def warden_sign_up_view(request, *args, **kwargs):
    user_form = WardenSignupForm(request.POST or None)

    if user_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.is_warden = True
        user.save()
        messages.success(request, 'You are successfully created an account, Now login to continue')
        return redirect('index')

    context = {
        'user_form': user_form,
    }
    return render(request, "main/warden_register.html", context)


@login_required
@student_required
def write_application(request):
    applications_form = LeaveApplication(request.POST or None)
    print(request.user)

    if applications_form.is_valid():

        application = applications_form.save(commit=False)
        application.student = Student.objects.get(
            user=UserProfile.objects.get(email=request.user))
        application.mentor = Student.objects.get(
            user=UserProfile.objects.get(email=request.user)).mentor
        application.save()

        messages.success(request, 'Your application was submitted successfully')

        return redirect('student-view')
    else:
        print(applications_form.errors)


    return render(request, 'main/application.html', {
        'application_form': applications_form
    })


@login_required
@student_required
def students_previous_app_status(request):
    applications = Applications.objects.filter(
        student=Student.objects.get(user=request.user))
    return render(request, 'main/previous_applications.html', {
        'applications': applications
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(email=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if user.is_mentor:
                    messages.success(request, 'You are successfully logged in')
                    return redirect('teacher-view')
                if user.is_student:
                    messages.success(request, 'You are successfully logged in')
                    return redirect('student-view')
                if user.is_warden:
                    messages.success(request, 'You are successfully logged in')
                    return redirect('warden-view')
            else:
                messages.error(request, 'This account is no longer active')
                return redirect('login')
        else:
            messages.error(request, 'Invalid login details')
            return redirect('login')
    else:
        return render(request, 'main/login.html')


def reset_password(request):
    if request.method == 'POST':

        reset_form = ResetPassword(data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        if(reset_form.is_valid()):
            user = UserProfile.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password was changed successfully')
            return redirect('login')

    else:
        reset_form = ResetPassword()

    return render(request, 'main/reset_pwd.html', {'reset_form': reset_form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You were logged out successfully')
    return redirect('/')


@login_required
@teacher_required
def students_leave(request):
    mentor = Mentor.objects.get(user=UserProfile.objects.get(
        email=request.user))
    leaves = Applications.objects.filter(mentor=mentor)
    return render(request, 'main/leave_requests.html', {
        'leaves': leaves
    })


@login_required
@teacher_required
def reject_leave_with_reason(request, pk):
    reject_form = RejectionForm(request.POST or None)

    if reject_form.is_valid():
        application = Applications.objects.get(pk=pk)
        application.rejected = True
        application.reason = reject_form.cleaned_data['reason']
        application.save()
        message.success(request, 'The application was rejected successfully')
        return redirect('requests')

    context = {
        'reject_form': reject_form,
    }
    return render(request, "main/reject_reason.html", context)


@login_required
@teacher_required
def accept_leave_with_rec(request, pk):
    rec_form = RecommendationForm(request.POST or None)

    if rec_form.is_valid():
        application = Applications.objects.get(pk=pk)
        application.approved = True
        application.recommendation = rec_form.cleaned_data['recommendation']
        application.message_to_parent = rec_form.cleaned_data['message_to_parent']
        application.save()
        subject = 'Hostel Leave Management'
        message_for_parents = rec_form.cleaned_data['message_to_parent']
        html = """\
                <html>
                  <body>
                    <p>"""+message_for_parents+"""<br>
                       <a href="http://127.0.0.1:8000/parent-approval/"""+str(pk)+"""/">Visit this link to acknowledge your childs leave request</a>
                    </p>
                  </body>
                </html>
                """
        student = Applications.objects.get(pk=pk).student
        parent = Parent.objects.get(student=student)
        recepient = parent.parent_mail
        msg = EmailMessage(subject, html, EMAIL_HOST_USER, [recepient])
        msg.content_subtype = "html"
        msg.send()
        messages.success(request, 'The application was successfully accepted and an email was send to your menties parents')
        return redirect('requests')

    context = {
        'rec_form': rec_form,
    }
    return render(request, "main/recommendation.html", context)

def parent_view(request, pk):
    application = Applications.objects.get(pk=pk)
    return render(request, 'main/parent_approval.html', {
        'application': application
    })

def parent_approvs_request(request, pk):
    application = Applications.objects.get(pk=pk)
    if application.parent_rejection == True:
        application.parent_rejection = False
    application.parent_approval = True
    application.save()
    messages.success(request, 'The request was acknowledged successfully')
    return redirect('parent-view', pk=pk)


def parent_rejects_request(request, pk):
    application = Applications.objects.get(pk=pk)
    application.parent_rejection = True
    application.save()
    messages.success(request, 'The request was rejected successfully (This decision can be changed by clicking on accepted button)')
    return redirect('parent-view', pk=pk)

@login_required
@warden_required
def warden_view(request):
    applications = Applications.objects.filter(approved=True, parent_approval=True)
    return render(request, 'main/warden_view.html', {
        'applications': applications
    })

@login_required
@warden_required
def students_to_leave_from_hostel(request):
    applications = Applications.objects.filter(approved=True, parent_approval=True)
    leave_filter = LeaveFilter(request.GET, queryset=applications)
    return render(request, 'main/list_of_students_to_leave.html', {
        'leave_filter': leave_filter
    })

@login_required
@warden_required
def start_leave(request, pk):
    application = Applications.objects.get(pk=pk)
    application.left_hostel = True
    application.living_date = datetime.datetime.now()
    application.save()

    student = Applications.objects.get(pk=pk).student
    parent_mail = Parent.objects.get(student=student).parent_mail
    mentor_mail = application.mentor.user.email

    subject = 'LEAVE MANAGEMENT SYSTEM'
    message_for_parent = 'Your ward {} has left hostel on {}'.format(application.student.user.name, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    message_for_mentor = 'Your mentie {} has left hostel on {}'.format(application.student.user.name, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    message1 = (subject, message_for_parent, EMAIL_HOST_USER, [parent_mail])
    message2 = (subject, message_for_mentor, EMAIL_HOST_USER, [mentor_mail])
    send_mass_mail((message1, message2, ), fail_silently=False)

    messages.success(request, 'The leave was started successfully')

    return redirect('students-leaving')


@login_required
@warden_required
def end_leave(request, pk):
    application = Applications.objects.get(pk=pk)
    application.returned_hostel = True
    application.returning_date = datetime.datetime.now()
    if application.till_date < datetime.date.today():
        application.is_delayed = True
    application.save()

    student = Applications.objects.get(pk=pk).student
    parent_mail = Parent.objects.get(student=student).parent_mail
    mentor_mail = application.mentor.user.email

    if application.is_delayed:
        subject = 'LEAVE MANAGEMENT SYSTEM'
        message_for_parent = 'Your ward {} was arrived late on {}.'.format(application.student.user.name, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        message_for_mentor = 'Your mentie {} was arrived late on {}'.format(application.student.user.name, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    else:
        subject = 'LEAVE MANAGEMENT SYSTEM'
        message_for_parent = 'Your ward {} was arrived on time at {}'.format(application.student.user.name, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        message_for_mentor = 'Your mentie {} was arrived on time at {}'.format(application.student.user.name, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    message1 = (subject, message_for_parent, EMAIL_HOST_USER, [parent_mail])
    message2 = (subject, message_for_mentor, EMAIL_HOST_USER, [mentor_mail])
    send_mass_mail((message1, message2, ), fail_silently=False)

    messages.success(request, 'The leave was ended successfully')

    return redirect('students-leaving')
