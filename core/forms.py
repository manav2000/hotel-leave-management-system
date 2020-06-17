from django import forms
from django.db import transaction
from django.core.validators import validate_email
import datetime
from .models import *


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_name()


class StudentSignUpForm(forms.ModelForm):
    mentor = UserModelChoiceField(
        queryset=Mentor.objects.all())
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput())
    parents_mail = forms.EmailField(validators=[validate_email])
    parent_name = forms.CharField()

    class Meta():
        model = UserProfile
        fields = ['name', 'email', 'password']

    def clean_conf_password(self):
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']

        if password != conf_password:
            raise forms.ValidationError('Both password fields should match')
        else:
            return conf_password

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
        Parent.objects.create(student=student,
                        parent_mail=self.cleaned_data.get('parents_mail'),
                        parent_name=self.cleaned_data.get('parent_name')
                        )

        return user


class TeacherSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = UserProfile
        fields = ['name', 'email', 'password']

    def clean_conf_password(self):
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']

        if password != conf_password:
            raise forms.ValidationError('Both password fields should match')
        else:
            return conf_password

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

    def clean_date_from(self):
        date_from = self.cleaned_data.get('date_from')
        print(date_from)
        print(datetime.date.today())
        date_now = datetime.date.today()
        if date_from >= date_now:
            print(date_from)
            return date_from
        else:
            print(date_from)
            raise forms.ValidationError('Provide a valide date')

    def clean_till_date(self):
        till_date = self.cleaned_data.get('till_date')
        date_now = datetime.date.today()
        print(till_date)

        if till_date >= date_now:
            return till_date
        else:
            raise forms.ValidationError('Provide a valide return date')



class RejectionForm(forms.ModelForm):
    class Meta():
        model = Applications
        fields = ['reason']


class RecommendationForm(forms.ModelForm):
    recommendation = forms.CharField(widget=forms.Textarea(attrs={'required': 'false'}))

    class Meta():
        model = Applications
        fields = ['recommendation', 'message_to_parent']


class WardenSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = UserProfile
        fields = ['name', 'email', 'password']

    def clean_conf_password(self):
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']

        if password != conf_password:
            raise forms.ValidationError('Both password fields should match')
        else:
            return conf_password

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_warden = True
        user.save()
        warden = Warden.objects.create(user=user)

        return user
