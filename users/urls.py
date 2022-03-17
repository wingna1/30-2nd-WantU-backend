from django.urls import path
from users.views import KakaoLoginView
 
urlpatterns = [
    path("/kakao/login", KakaoLoginView.as_view()),
]