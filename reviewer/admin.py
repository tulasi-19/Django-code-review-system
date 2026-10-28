from django.contrib import admin
from .models import CodeSubmission, Review


@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "language", "status", "created_at")
    list_filter = ("language", "status")
    search_fields = ("title", "user__username")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("submission", "score", "issues_found", "engine_used", "created_at")
    list_filter = ("engine_used",)
