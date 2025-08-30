from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application
from .forms import JobForm, ApplicationForm

# Job list with search & filters
def job_list(request):
    jobs = Job.objects.all()

    # Get filter values from GET request
    search = request.GET.get('search')
    location = request.GET.get('location')
    company = request.GET.get('company')

    # Apply filters
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    if company:
        jobs = jobs.filter(company__icontains=company)

    return render(request, "jobs/job_list.html", {"jobs": jobs})

# Job detail page
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, candidate=request.user).exists()
    return render(request, "jobs/job_detail.html", {"job": job, "has_applied": has_applied})

# Recruiter dashboard
@login_required
def recruiter_dashboard(request):
    if request.user.role != "recruiter":
        return redirect("job_list")

    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, "jobs/recruiter_dashboard.html", {"jobs": jobs})


@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = Application.objects.filter(job=job)
    return render(request, "jobs/job_applicants.html", {"job": job, "applications": applications})



@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()
        messages.success(request, f"Application status updated to {status}.")
    return redirect('job_applicants', job_id=application.job.id)




# Candidate dashboard
@login_required
def candidate_dashboard(request):
    if request.user.role != "candidate":
        return redirect("job_list")  # prevent recruiters from seeing this page
    
    applications = Application.objects.filter(candidate=request.user)
    return render(request, "jobs/candidate_dashboard.html", {"applications": applications})

# Create a job (recruiter only)
@login_required
def job_create(request):
    if request.user.role != "recruiter":
        return redirect("job_list")
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect("job_list")
    else:
        form = JobForm()
    return render(request, "jobs/job_form.html", {"form": form})

# Apply for a job (candidate only)
@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    # only candidates can apply
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can apply for jobs.")
        return redirect("job_detail", pk=pk)

    # prevent duplicate applications
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.info(request, "You already applied for this job.")
        return redirect("job_detail", pk=pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect("job_detail", pk=pk)
    else:
        form = ApplicationForm()
    return render(request, "jobs/job_apply.html", {"form": form, "job": job})
