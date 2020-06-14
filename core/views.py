from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import student_required, teacher_required
from .models import *
from .forms import *

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
        return redirect('index')

    context = {
        'user_form': user_form,
    }
    return render(request, "main/techer_register.html", context)


@login_required
@student_required
def write_application(request):
    applications_form = LeaveApplication(request.POST or None)
    print(request.user)

    if applications_form.is_valid():

        print('success')
        application = applications_form.save(commit=False)
        application.student = Student.objects.get(
            user=UserProfile.objects.get(email=request.user))
        application.mentor = Student.objects.get(
            user=UserProfile.objects.get(email=request.user)).mentor
        print(Student.objects.get(
            user=UserProfile.objects.get(email=request.user)).mentor.students)
        application.save()
        return redirect('student-view')

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
                    return redirect('teacher-view')
                else:
                    return redirect('student-view')

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login to your account")
            return HttpResponse('Invalid login details')

    else:
        return render(request, 'main/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
@teacher_required
def students_leave(request):
    print(request.user)
    mentor = Mentor.objects.get(user=UserProfile.objects.get(
        email=request.user))
    print(mentor)
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
        application.save()
        return redirect('requests')

    context = {
        'rec_form': rec_form,
    }
    return render(request, "main/recommendation.html", context)
