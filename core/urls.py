from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('student-sign-up/', student_sign_up_view),
    path('teacher-sign-up/', teacher_sign_up_view),
    path('write-application/', write_application, name='application'),
    path('your-applications/', students_previous_app_status,
         name='application-status'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('teacher/', teacher_view, name="teacher-view"),
    path('student/', student_view, name="student-view"),
    path('leave-requests/', students_leave, name='requests'),
    # path('accept/<int:pk>/', accept_leave_without_rec, name='accept'),
    # path('reject/<int:pk>/', reject_leave_without_reason, name='reject'),
    path('accept_rec/<int:pk>/', accept_leave_with_rec, name='accept_rec'),
    path('reject_reason/<int:pk>/', reject_leave_with_reason, name='reject_reason'),
]
