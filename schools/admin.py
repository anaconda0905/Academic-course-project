from django.contrib import admin
# Register your models here.
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin

from schools.models import School, SchoolStudent, Teacher


@admin.register(School)
class SchoolModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    list_display = ["user_name", "name", "user_email"]
    list_display_links = ('user_name', 'user_email')
    history_list_display = ["status"]
    search_fields = ['user__username']

    def user_name(self, instance):
        return instance.user.username

    def user_email(self, instance):
        return instance.user.email


@admin.register(SchoolStudent)
class StudentModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(Teacher)
class TeacherAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']
