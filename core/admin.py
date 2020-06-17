from django.contrib import admin
from .models import *

# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_from', 'till_date', )
    fieldsets = [
        ('Student info', {'fields': ['mentor', 'student']}),
        ('Purpose', {'fields': ['purpose']}),
        ('Date information', {'fields': ['date_from', 'till_date'], 'classes': ['collapse']}),
        ('Boolean fields', {'fields':['approved', 'parent_approval', 'rejected', 'parent_rejection',
         'left_hostel', 'returned_hostel', 'is_delayed'], 'classes': ['collapse']}),
        ('Additional info', {'fields': ['reason', 'recommendation', 'message_to_parent']})
    ]
    list_filter = ['date_from', 'till_date', 'left_hostel', 'returned_hostel']
    search_fields = ['date_from', 'till_date']



admin.site.register(UserProfile)
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Applications, ApplicationAdmin)
admin.site.register(Warden)
