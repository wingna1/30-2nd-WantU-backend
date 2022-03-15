from django.urls    import path
from cv.views       import ResumeDownloadView, ResumeUploadView

urlpatterns = [
    path('', ResumeUploadView.as_view()),
    path("/<int:resume_pk>", ResumeDownloadView.as_view())
]