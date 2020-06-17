from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('student-sign-up/', student_sign_up_view),
    path('teacher-sign-up/', teacher_sign_up_view),
    path('warden-sign-up/', warden_sign_up_view),
    path('write-application/', write_application, name='application'),
    path('your-applications/', students_previous_app_status,
         name='application-status'),
    path('login/', login_view, name='login'),
    path('reset_pwd/', reset_password, name='reset'),
    path('logout/', logout_view, name='logout'),
    path('teacher/', teacher_view, name="teacher-view"),
    path('student/', student_view, name="student-view"),
    path('warden/', warden_view, name="warden-view"),
    path('leave-requests/', students_leave, name='requests'),
    path('accept_rec/<int:pk>/', accept_leave_with_rec, name='accept_rec'),
    path('reject_reason/<int:pk>/', reject_leave_with_reason, name='reject_reason'),
    path('parent-approval/<int:pk>/', parent_view, name="parent-view"),
    path('parent-approves/<int:pk>/', parent_approvs_request, name="parent-approves"),
    path('parent-rejects/<int:pk>/', parent_rejects_request, name="parent-rejects"),
    path('students-leaving/', students_to_leave_from_hostel, name="students-leaving"),
    path('start-leave/<int:pk>/', start_leave, name="start-leave"),
    path('end-leave/<int:pk>/', end_leave, name="end-leave"),
]
