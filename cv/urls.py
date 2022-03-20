from django.urls    import path
from cv.views       import ResumeInfoView, ResumeUploadView, ResumeListView

urlpatterns = [
    path('', ResumeUploadView.as_view()),
    path("/list/<str:resume_pk>", ResumeInfoView.as_view()),
    path('/list', ResumeListView.as_view()),
]