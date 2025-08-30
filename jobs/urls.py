from django.urls import path
from .views import job_list, job_create,job_detail, apply_job
from .views import candidate_dashboard
from jobs import views

urlpatterns = [
    path("", job_list, name="job_list"),
    path("create/", job_create, name="job_create"),
    path("<int:pk>/", job_detail, name="job_detail"),
    path("<int:pk>/apply/", apply_job, name="job_apply"),
    path("candidate/dashboard/", candidate_dashboard, name="candidate_dashboard"),
    path("recruiter/dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("job/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("application/<int:app_id>/status/<str:status>/", views.update_application_status, name="update_application_status"),

]
