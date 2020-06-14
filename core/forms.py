from django import forms
from django.db import transaction
from .models import *


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_name()


class StudentSignUpForm(forms.ModelForm):
    mentor = UserModelChoiceField(
        queryset=Mentor.objects.all())

    password = password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = UserProfile
        fields = ['name', 'email', 'password']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        print(self.cleaned_data.get('mentor').user.name)
        mentor_name = self.cleaned_data.get('mentor').user
        student = Student.objects.create(
            user=user, mentor=self.cleaned_data.get('mentor'))
        mentor = Mentor.objects.get(user=mentor_name)
        mentor.students.add(student)

        return user


class TeacherSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = UserProfile
        fields = ['name', 'email', 'password']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_mentor = True
        user.save()
        mentor = Mentor.objects.create(user=user)

        return user


class LeaveApplication(forms.ModelForm):
    date_from = forms.DateField(widget=forms.SelectDateWidget())
    till_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta():
        model = Applications
        fields = ['purpose', 'date_from', 'till_date']


class RejectionForm(forms.ModelForm):
    class Meta():
        model = Applications
        fields = ['reason']


class RecommendationForm(forms.ModelForm):
    class Meta():
        model = Applications
        fields = ['recommendation']
