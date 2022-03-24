from django.urls import path, include

urlpatterns = [
    path("users", include("users.urls")),
    path('applications', include('applications.urls')),
    path("jobs", include("jobs.urls")),
    path('cv', include('cv.urls'))
]
