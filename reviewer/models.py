from django.conf import settings
from django.db import models


LANGUAGE_CHOICES = [
    ("python", "Python"),
    ("java", "Java"),
    ("c", "C"),
    ("cpp", "C++"),
    ("javascript", "JavaScript"),
    ("other", "Other"),
]

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("reviewed", "Reviewed"),
    ("failed", "Failed"),
]


class CodeSubmission(models.Model):
    """A single piece of source code submitted by a student for review."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions"
    )
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default="python")
    code = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_language_display()}) - {self.user.username}"


class Review(models.Model):
    """The automated feedback generated for a code submission."""

    submission = models.OneToOneField(
        CodeSubmission, on_delete=models.CASCADE, related_name="review"
    )
    feedback = models.TextField()
    score = models.PositiveIntegerField(default=0, help_text="Overall quality score out of 100")
    issues_found = models.PositiveIntegerField(default=0)
    engine_used = models.CharField(
        max_length=20,
        choices=[("gpt", "GPT-based"), ("heuristic", "Static analysis")],
        default="heuristic",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.submission.title}"
