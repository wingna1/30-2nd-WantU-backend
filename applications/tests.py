import jwt, uuid

from django.test  import TestCase, Client

from cv.models    import Resume
from .models      import Applicant,ApplicationStatus,Application
from users.models import User
from jobs.models  import JobPosition, JobCategory, Company

from my_settings  import SECRET_KEY, ALGORITHM

class StatusViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_list = [User(
            id                = 1,
            kakao_nickname    = "testman",
            kakao_email       = "www.email.com",
            kakao_id          = 12345678,
            profile_image_url = "www.test.1"
            ) ,
            User(
            id                = 2,
            kakao_nickname    = "testman2",
            kakao_email       = "www.email2.com",
            kakao_id          = 123456789,
            profile_image_url = "www.test.2"
            )]

        cls.user     = User.objects.bulk_create(cls.user_list)
        cls.token    = jwt.encode({'id' :User.objects.get(id=1).id}, SECRET_KEY, algorithm = ALGORITHM)
        cls.header   = {'HTTP_Authorization' : cls.token}
        cls.payload  = jwt.decode(cls.token, SECRET_KEY, algorithms = ALGORITHM)

        cls.token2    = jwt.encode({'id' :User.objects.get(id=2).id}, SECRET_KEY, algorithm = ALGORITHM)
        cls.header2   = {'HTTP_Authorization' : cls.token2}
        cls.payload2  = jwt.decode(cls.token2, SECRET_KEY, algorithms = ALGORITHM)

        cls.resume = Resume.objects.create(
                id       = 1,
                name     = "test1",
                file_url = "www.test1.com",
                user     = cls.user[0],
                uuid     = str(uuid.uuid4())
            ),

        cls.applicant = Applicant.objects.create(
            id      =1,
            user_id =1
        )

        cls.application_status = ApplicationStatus.objects.create(id=1,status="applied")

        cls.job_category       = JobCategory.objects.create(id=1 ,name="Server") 

        cls.company            = Company.objects.create(id=1,name="google", location="LA", average_salary=3000)  

        cls.job_positions      = JobPosition.objects.create(
            id=1,
            title           = "BackEnd",
            content         = "content",
            due_date        = "2022-05-23",
            job_category_id = 1,
            company_id      = 1
        )

        cls.application = Application.objects.create(
            id              = 1 ,
            applicant_id    = 1,
            resume_id       = 1,
            job_position_id = 1,
            status_id       = 1
        )

    def test_success_get_application_status(self):
            client = Client()

            response = client.get('/applications', **self.header)

            
            result ={
                    "result": {
                        "accepted"       : 0,
                        "applied"        : 1,
                        "document_passed": 0,
                        "rejection"      : 0,
                        "total"          : 1
                    }
                }

            self.assertEqual(response.json(), result)

            self.assertEqual(response.status_code, 200)

    def test_fail_get_applications_status_no_appplication_record(self):
            client = Client()

            response = client.get('/applications', **self.header2)

            self.assertEqual(response.json(), {'result':"NO valid application"})

            self.assertEqual(response.status_code, 404)


class CompanyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_list = [User(
            id                = 1,
            kakao_nickname    = "testman",
            kakao_email       = "www.email.com",
            kakao_id          = 12345678,
            profile_image_url = "www.test.1"
            ) ,
            User(
            id                = 2,
            kakao_nickname    = "testman2",
            kakao_email       = "www.email2.com",
            kakao_id          = 123456789,
            profile_image_url = "www.test.2"
            )]

        cls.user     = User.objects.bulk_create(cls.user_list)
        cls.token    = jwt.encode({'id' :User.objects.get(id=1).id}, SECRET_KEY, algorithm = ALGORITHM)
        cls.header   = {'HTTP_Authorization' : cls.token}
        cls.payload  = jwt.decode(cls.token, SECRET_KEY, algorithms = ALGORITHM)

        cls.token2    = jwt.encode({'id' :User.objects.get(id=2).id}, SECRET_KEY, algorithm = ALGORITHM)
        cls.header2   = {'HTTP_Authorization' : cls.token2}
        cls.payload2  = jwt.decode(cls.token2, SECRET_KEY, algorithms = ALGORITHM)

        cls.resume = Resume.objects.create(
                id       = 1,
                name     = "test1",
                file_url = "www.test1.com",
                user     = cls.user[0],
                uuid     = str(uuid.uuid4())
            ),

        cls.applicant = Applicant.objects.create(
            id     =1,
            user_id=1
        )

        cls.application_status = ApplicationStatus.objects.create(status="applied")

        cls.job_category = JobCategory.objects.create(name="Server") 

        cls.company = Company.objects.create(name="google", location="LA", average_salary=3000)  

        cls.job_positions = JobPosition.objects.create(
            title          = "BackEnd",
            content        = "content",
            due_date       = "2022-05-23",
            job_category_id= 1,
            company_id     = 1
        )

        cls.application = Application.objects.create(
            id              = 1 ,
            applicant_id    = 1,
            resume_id       = 1,
            job_position_id = 1,
            status_id       = 1
        )

    def test_success_get_companies_match_with_apply_status(self):
        client = Client()

        response = client.get('/applications/status/applied', **self.header)

        result = {
                    "result": [
                        {
                            "company_name": "google",
                            "category"    : "Server",
                            "applied_date": self.application.created_at.strftime('%Y.%m.%d'),
                            "apply_status": "applied"
                        }]
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)
    
    def test_fail_get_companies_match_with_apply_status_user_has_no_application_record(self):
        client = Client()

        response = client.get('/applications/status/applied', **self.header2)

        self.assertEqual(response.json(), {'result':None})
        self.assertEqual(response.status_code, 404)


