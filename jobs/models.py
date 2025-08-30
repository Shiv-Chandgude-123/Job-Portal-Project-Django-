from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from accounts.models import User


def generate_job_code():
    """Generate unique job code like J8K2Q9ZL"""
    return get_random_string(8).upper()


class Job(models.Model):
    JOB_TYPES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
    ]

    WORK_MODES = [
        ("onsite", "On-site"),
        ("remote", "Remote"),
        ("hybrid", "Hybrid"),
    ]

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    # --- New fields ---
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default="full_time")
    work_mode = models.CharField(max_length=20, choices=WORK_MODES, default="onsite")
    openings = models.PositiveIntegerField(default=1)
    job_code = models.CharField(max_length=12, unique=True, editable=False, blank=True, default="")
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.job_code:
            code = generate_job_code()
            while Job.objects.filter(job_code=code).exists():
                code = generate_job_code()
            self.job_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.job_code})"


class Application(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.candidate.username} applied for {self.job.title}"


class SavedJob(models.Model):
    """Candidate wishlist / saved jobs"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saves")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
