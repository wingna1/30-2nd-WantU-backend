from django.urls    import path
from applications.views import ApplyView, StatusView, CompanyView

urlpatterns = [
    path('', StatusView.as_view()),
    path('/status/<str:status>', CompanyView.as_view()),
    path('/submission', ApplyView.as_view())
]
