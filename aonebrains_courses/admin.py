from django.contrib import admin
# Register your models here.
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import OpenCourse, OpenSubject, OpenModule, OpenContent, AVideo, AImage, AFile, AText


@admin.register(OpenCourse)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(OpenSubject)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(OpenModule)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(OpenContent)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(AText)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(AFile)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(AVideo)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(AImage)
class YourModelAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']
