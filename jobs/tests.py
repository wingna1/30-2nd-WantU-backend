import jwt

from datetime       import datetime, timedelta
from django.test    import Client, TestCase

from django.utils   import dateparse, timezone
from unittest       import mock

from my_settings            import SECRET_KEY, ALGORITHM
from applications.models    import Application, Applicant, ApplicationStatus
from cv.models              import Resume
from jobs.models            import JobPosition, JobCategory, Company, CompanyImage, Tag, TagNotification
from users.models           import User

class JobPositionTest(TestCase):
    @classmethod
    def setUpTestData(self):    
        User.objects.create(
            id                = 1,
            kakao_nickname    = "핑핑이",
            kakao_email       = "pingping@gmail.com",
            kakao_id          = 123456789,
            profile_image_url = "http://111.jpg"
        )
        Applicant.objects.create(
            id      = 1,
            user_id = 1
        )
        Resume.objects.create(
            id         = 1,
            name       = "이력서최종",
            file_url   = "https://www.robertwalters.co.kr/content/dam/robert-walters/country/korea/files/resume/RESUME_Templete_1_KR.jpg",
            uuid       = "8b34d6f8-4a0f-4e77-9b50-22d562708fe5",
            is_deleted = False,
            user_id    = 1
        )
        JobCategory.objects.create(
            id   = 1,
            name = "Web Backend"
        )
        Company.objects.create(
            id             = 1,
            name           = "테슬라",
            location       = "미국 텍사스",
            average_salary = 13500
        )
        CompanyImage.objects.create(
            id         = 1,
            company_id = 1,
            image_url  = "https://raw.githubusercontent.com/wingna1/wantuPicbase/main/tesla1.jpg"
        )
        Tag.objects.create(
            id   = 1,
            name = "#자율복장"
        )
        JobPosition.objects.create(
            id              = 1,
            title           = "개발자 구합니다",
            content         = "4대보험 가능! 근로계약서 작성 노동청 앞에서 함!",
            due_date        = "2022-04-02",
            company_id      = 1,
            job_category_id = 1
        )
        JobPosition.objects.create(
            id              = 2,
            title           = "개발자 환영! 대환영!",
            content         = "세상에 없던 서비스 등장! 함께하실 개발자를 구합니다",
            due_date        = "2022-04-06",
            company_id      = 1,
            job_category_id = 1
        )
        TagNotification.objects.create(
            id              = 1,
            tag_id          = 1,
            job_position_id = 1
        )
        ApplicationStatus.objects.create(
            id     = 1,
            status = "applied"
        )
        Application.objects.create(
            id              = 1,
            applicant_id    = 1,
            resume_id       = 1,
            job_position_id = 1,
            status_id       = 1,
        )

    def tearDown(self):
        JobPosition.objects.all().delete()

    def test_success_for_getting_user_data_about_job_position(self):
        client   = Client()
        token    = jwt.encode({"id":1, "exp":datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)
        headers  = {"HTTP_Authorization":token}
        response = client.get("/jobs/1/user", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results":{
            "is_applied"    :True,
            "kakao_email"   :"pingping@gmail.com",
            "kakao_nickname":"핑핑이",
            "resumes"       :[
                {
                    "name"        :"이력서최종",
                    "created_date":response.json()["results"]["resumes"][0]["created_date"],
                    "uuid"        :"8b34d6f8-4a0f-4e77-9b50-22d562708fe5"
                }
            ]
        }})

    def test_fail_for_wrong_users_token_for_getting_user_data_about_job_position(self):
        client   = Client()
        token    = jwt.encode({"id":2, "exp":datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)
        headers  = {"HTTP_Authorization":token}
        response = client.get("/jobs/1/user", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_USER"})

    def test_success_for_getting_job_position_data(self):
        client   = Client()
        response = client.get("/jobs/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results": {
                "job_position_id"       :1,
                "job_categories_name"   :"Web Backend",
                "due_date"              :"2022-04-02",
                "title"                 :"개발자 구합니다",
                "content"               :"4대보험 가능! 근로계약서 작성 노동청 앞에서 함!",
                "company_name"          :"테슬라",
                "company_location"      :"미국 텍사스",
                "company_average_salary":"13500.00000",
                "tags"                  :["#자율복장"],
                "images"                :["https://raw.githubusercontent.com/wingna1/wantuPicbase/main/tesla1.jpg"]
            }})

    def test_fail_for_getting_non_existing_job_position_data(self):
        client   = Client()
        response = client.get("/jobs/100")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Data Does Not Exist"})

    def test_success_for_getting_job_list_data_without_filter(self):
        client   = Client()
        response = client.get("/jobs")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results": {
                "total_count":2,
                "list_data":[
                {
                    "job_position_id" :1,
                    "title"           :"개발자 구합니다",
                    "company_name"    :"테슬라",
                    "company_location":"미국 텍사스",
                    "company_image"   :"https://raw.githubusercontent.com/wingna1/wantuPicbase/main/tesla1.jpg"
                },
                {
                    "job_position_id" :2,
                    "title"           :"개발자 환영! 대환영!",
                    "company_name"    :"테슬라",
                    "company_location":"미국 텍사스",
                    "company_image"   :"https://raw.githubusercontent.com/wingna1/wantuPicbase/main/tesla1.jpg"
                }
            ]
        }})

    def test_success_for_getting_job_list_data_with_three_filters_one_sort_one_page(self):
        client       = Client()
        query_string = "?category=0&tag=0&area=미국&sort=id&offset=0&limit=1"
        response     = client.get("/jobs" + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results":{
                "total_count":2,
                "list_data":[
                {
                    "job_position_id" :1,
                    "title"           :"개발자 구합니다",
                    "company_name"    :"테슬라",
                    "company_location":"미국 텍사스",
                    "company_image"   :"https://raw.githubusercontent.com/wingna1/wantuPicbase/main/tesla1.jpg"
                }
            ]
        }})

    def test_fail_for_getting_job_list_data_with_wrong_filter(self):
        client       = Client()
        query_string = "?category=100&tag=100&area=남극&sort=1"
        response     = client.get("/jobs" + query_string)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"Invalid Type of Parameter"})
