from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "salary", "recruiter")  # columns in admin
    list_filter = ("company", "location")  # sidebar filters
    search_fields = ("title", "company", "recruiter__username")  # search box
    ordering = ("-id",)  # newest first


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "candidate", "status", "applied_at")  # show these columns
    list_filter = ("status", "applied_at")  # filter options
    search_fields = ("job__title", "candidate__username")  # search by job/candidate
    ordering = ("-applied_at",)  # latest applications first
