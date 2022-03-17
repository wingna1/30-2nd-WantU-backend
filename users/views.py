import requests, jwt

from datetime               import datetime, timedelta
from django.http            import JsonResponse
from django.views           import View
from requests.exceptions    import Timeout

from my_settings      import SECRET_KEY, ALGORITHM
from users.models     import User

class KakaoLoginView(View):
    def get(self, request):
        try:
            access_token = request.headers.get("Authorization", None)

            if access_token == None:
                return JsonResponse({"message":"Invalid Access Token"}, status=401)

            kakao_user_api   = "https://kapi.kakao.com/v2/user/me"
            headers          = {"Authorization":f"Bearer ${access_token}"}
            user_information = requests.get(kakao_user_api, headers=headers, timeout=5).json()

            kakao_id          = user_information["id"]
            kakao_email       = user_information["kakao_account"]["email"]
            profile_image_url = user_information["properties"]["profile_image"]
            kakao_nickname    = user_information["properties"]["nickname"]

            user, created = User.objects.update_or_create( 
                kakao_id = kakao_id, 
                defaults = {"kakao_nickname":kakao_nickname, "profile_image_url":profile_image_url, "kakao_email":kakao_email}
            )

            token = jwt.encode({"id":user.id, "exp":datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)

            results = {
                "token"            :token,
                "kakao_email"      :user.kakao_email,
                "kakao_nickname"   :user.kakao_nickname,
                "profile_image_url":user.profile_image_url
            }
            return JsonResponse({"results":results}, status=200)
        except Timeout:
            return JsonResponse({"message":"Time Out"}, status=408)
        except KeyError:
            return JsonResponse({"message":"Key Error"}, status=400)
