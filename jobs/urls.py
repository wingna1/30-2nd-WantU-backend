from django.urls import path

from jobs.views  import JobPositionDetailView, JobPositionListView, JobPositionUserDataView
 
urlpatterns = [
    path("/<int:job_position_id>", JobPositionDetailView.as_view()),
    path("/<int:job_position_id>/user", JobPositionUserDataView.as_view()),
    path("", JobPositionListView.as_view()),
]