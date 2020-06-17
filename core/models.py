from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class UserProfileManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, email, name, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser):
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_warden = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


class Mentor(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    students = models.ManyToManyField(
        'Student', related_name='menties', blank=True)

    def __str__(self):
        return str(self.user)

    def get_name(self):
        return self.user.name


class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    def mentor_name(self):
        return str(self.mentor.user.name)


class Applications(models.Model):
    mentor = models.ForeignKey(
        Mentor, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    purpose = models.TextField()
    date_from = models.DateField()
    till_date = models.DateField()
    approved = models.BooleanField(default=False)
    parent_approval = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    parent_rejection = models.BooleanField(default=False)
    left_hostel = models.BooleanField(default=False)
    returned_hostel = models.BooleanField(default=False)
    living_date = models.DateTimeField(auto_now_add=True, blank=True)
    returning_date = models.DateTimeField(auto_now_add=True, blank=True)
    is_delayed = models.BooleanField(default=False)
    reason = models.TextField()
    recommendation = models.TextField()
    message_to_parent = models.TextField()

    def __str__(self):
        return "application from {} to his mentor {}".format(self.student.user.name, self.mentor.user.name)

    def mentor_name(self):
        return self.mentor.user.name

    def student_name(self):
        return str(self.student.user.name)


class Parent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent_mail = models.EmailField(max_length=255)
    parent_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.parent_name)

    def parents_child_name(self):
        return str(self.student.user.name)


class Warden(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.name)
