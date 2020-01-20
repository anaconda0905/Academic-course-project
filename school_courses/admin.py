from django.contrib import admin
# Register your models here.
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import SVideo, SImage, SFile, SText, SchoolCourse, SchoolModule, SchoolContent, SchoolSubject


@admin.register(SchoolCourse)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SchoolSubject)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SchoolModule)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SchoolContent)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SText)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SFile)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SVideo)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SImage)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']
