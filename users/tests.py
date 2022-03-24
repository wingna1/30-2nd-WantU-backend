import jwt

from django.test    import Client, TestCase
from unittest.mock  import MagicMock, patch

from datetime       import datetime, timedelta
from my_settings    import SECRET_KEY, ALGORITHM
from users.models   import User

class KakaoLoginTest(TestCase):
    @classmethod
    def setUpTestData(self):
        User.objects.create(
            id                = 1,
            kakao_nickname    = "핑핑이",
            kakao_email       = "pingping@gmail.com",
            kakao_id          = 1234567,
            profile_image_url = "http://111.jpg"
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_login_success_for_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":1234567,
                    "properties":{
                        "profile_image":"http://111.jpg",
                        "nickname"     :"핑핑이"
                    },
                    "kakao_account":{
                        "email":"pingping@gmail.com"
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers  = {"HTTP_Authorization":"fakeTokenforTest"}
        response = client.get("/users/kakao/login", **headers)

        response_token = response.json()["results"]["token"]
        payload        = jwt.decode(response_token, SECRET_KEY, ALGORITHM)  
        token          = jwt.encode({"id":payload["id"], "exp":datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results":{
                "token"            :token,
                "kakao_email"      :"pingping@gmail.com",
                "kakao_nickname"   :"핑핑이",
                "profile_image_url":"http://111.jpg"
            }
        })

    @patch("users.views.requests")
    def test_fail_for_absence_of_kakao_token(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":1234567,
                    "properties":{
                        "profile_image":"http://111.jpg",
                        "nickname"     :"핑핑이"
                    },
                    "kakao_account":{
                        "email":"pingping@gmail.com"
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        response = client.get("/users/kakao/login")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message":"Invalid Access Token"})

    @patch("users.views.requests")
    def test_login_fail_for_invalid_user_information_from_kakao(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "properties":{
                        "profile_image":"http://111.jpg"
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        headers  = {"HTTP_Authorization":"fakeTokenforTest"}
        response = client.get("/users/kakao/login", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"Key Error"})

    @patch("users.views.requests")
    def test_login_fail_for_time_out(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":1234567,
                    "properties":{
                        "profile_image":"http://111.jpg",
                        "nickname"     :"핑핑이"
                    },
                    "kakao_account":{
                        "email":"pingping@gmail.com"
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        headers  = {"HTTP_Authorization":"fakeTokenforTest"}
        response = client.get("/users/kakao/login", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"Time Out"})

    @patch("users.views.requests")
    def test_update_success_for_existing_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":1234567,
                    "properties":{
                        "profile_image":"http://1313.jpg",
                        "nickname"     :"세젤귀 핑핑"
                    },
                    "kakao_account":{
                        "email":"pingping@gmail.com"
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers  = {"HTTP_Authorization":"fakeTokenforTest"}
        response = client.get("/users/kakao/login", **headers)

        response_token = response.json()["results"]["token"]
        payload        = jwt.decode(response_token, SECRET_KEY, ALGORITHM)  
        token          = jwt.encode({"id":payload["id"], "exp":datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results":{
                "token"            :token,
                "kakao_email"      :"pingping@gmail.com",
                "kakao_nickname"   :"세젤귀 핑핑",
                "profile_image_url":"http://1313.jpg"
            }
        })
