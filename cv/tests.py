import jwt, uuid

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import  SimpleUploadedFile
from users.models                   import User
from .models                        import Resume

from my_settings import SECRET_KEY, ALGORITHM

# Create your tests here.
class ResumeUploadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id                = 1,
            kakao_nickname    = "testman",
            kakao_id          = 12345678,
            profile_image_url = "www.test.1"
            ) 
        cls.token    = jwt.encode({'id' :User.objects.get(id=1).id}, SECRET_KEY, algorithm = ALGORITHM)
        cls.header   = {'HTTP_Authorization' : cls.token}
        cls.payload  = jwt.decode(cls.token, SECRET_KEY, algorithms = ALGORITHM)

    def test_success_upload_resume_via_s3_post(self):
        client = Client()

        data = {
            'name'     : 'dj1.png',
            'file_url' : 'https://wantubucket1.s3.ap-northeast-2.amazonaws.com/dj1.png',
            'user'     : self.user,
            'filename' : SimpleUploadedFile(name="dj1.png", content=b"", content_type="*") 
            }
        
        response = client.post('/cv', data=data, **self.header)

        self.assertEqual(response.json(),
            {
                'message' : 'upload success'
            }
        )

        self.assertEqual(response.status_code, 201)
 

    def test_fail_upload_resume_via_s3_post_file_with_invalid_request(self):
        client = Client()
        
        data = {
            'name'      : 'dj1.png',
            'file_url'  : 'https://wantubucket1.s3.ap-northeast-2.amazonaws.com/dj1.png',
            'user'      : self.user,
            'file'      : SimpleUploadedFile(name="dj1.png", content=b"", content_type="*") 
            }

        response = client.post('/cv', data=data, **self.header)

        self.assertEqual(response.json(),
            {
                'message' : 'Key error'
            }
        )

        self.assertEqual(response.status_code, 400)

class ResumeInfoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id                = 1,
            kakao_nickname    = "testman",
            kakao_id          = 12345678,
            profile_image_url = "www.test.1"
            ) 
        cls.token    = jwt.encode({'id' :User.objects.get(id=1).id}, SECRET_KEY, algorithm = ALGORITHM)
        cls.header   = {'HTTP_Authorization' : cls.token}
        cls.payload  = jwt.decode(cls.token, SECRET_KEY, algorithms = ALGORITHM)

        cls.resume_list = [
            Resume(
                id       = 1,
                name     = "test1",
                file_url = "www.test1.com",
                user     = cls.user,
                uuid     = str(uuid.uuid4())
            ),
            Resume(
                id       = 2,
                name     = "test2",
                file_url = "www.test2.com",
                user     = cls.user,
                uuid     = str(uuid.uuid4())
            )
        ]

        cls.resume = Resume.objects.bulk_create(cls.resume_list)

    def test_success_download_resume_from_wantu_get(self):
        client   = Client()

        response = client.get('/cv/1',  **self.header)
        
        self.assertEqual(response.json(),{"message":"www.test1.com"})

        self.assertEqual(response.status_code, 200)

    def test_fail_download_resume_from_wantu_get_due_to_wrong_resume_pk_None_returned(self):
            client   = Client()

            response = client.get('/cv/500',  **self.header)

            self.assertEqual(response.json(),{'message': 'Invalid resume_pk'})

            self.assertEqual(response.status_code, 404) 

    def test_success_change_resume_name_in_wantu_patch(self):
            client = Client()

            data = {
                "name":"이름변경"
            }

            response = client.patch('/cv/1',  data=data, content_type='application/json',**self.header)

            self.assertEqual(response.status_code, 201)

    def test_fail_changing_resume_name_dueto_invalid_resume_pk(self):
        client = Client()
        
        data = {
            "name":"이름변경"
        }

        response = client.patch('/cv/5',  data=data, content_type='application/json',**self.header)

        self.assertEqual(response.json(), {'message': 'Invalid resume_pk'})

        self.assertEqual(response.status_code, 404)

    def test_fail_changing_resume_name_dueto_keyerror(self):
        client = Client()
        
        data = {
            'na2me':'이름변경'
        }

        response = client.patch('/cv/1',  data=data, content_type='application/json',**self.header)

        self.assertEqual(response.json(), {"message":"Key Error"})

        self.assertEqual(response.status_code, 400)

    def test_success_delete_resume_delete(self):
        client = Client()

        response = client.delete('/cv/1', **self.header)

        self.assertEqual(response.status_code, 200)

    def test_fail_delete_resume_dueto_invalid_resume_pk(self):
        client = Client()

        response = client.delete('/cv/5', **self.header)      

        self.assertEqual(response.json(), {'message':'Invalid resume_pk'})

        self.assertEqual(response.status_code, 404)

class ResumeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
            cls.user = User.objects.create(
                id                = 1,
                kakao_nickname    = "testman",
                kakao_id          = 12345678,
                profile_image_url = "www.test.1"
                ) 
            cls.token    = jwt.encode({'id' :User.objects.get(id=1).id}, SECRET_KEY, algorithm = ALGORITHM)
            cls.header   = {'HTTP_Authorization' : cls.token}
            cls.payload  = jwt.decode(cls.token, SECRET_KEY, algorithms = ALGORITHM)


            cls.resume_list = [
                Resume(
                    id      = 1,
                    name    = "test1",
                    file_url= "www.test1.com",
                    user    = cls.user,
                    uuid    = str(uuid.uuid4())
                ),
                Resume(
                    id      =2,
                    name    = "test2",
                    file_url= "www.test2.com",
                    user    = cls.user,
                    uuid    = str(uuid.uuid4())
                )
            ]

            cls.resumes = Resume.objects.bulk_create(cls.resume_list)

    def test_success_displaying_resume_list_get(self):
        client = Client()
    
        response = client.get('/cv/list', **self.header)
        
        result = [{
            "id"          : resume.id,
            "name"        : resume.name,
            "created_date": resume.created_at.strftime('%Y.%m.%d')
        } for resume in self.resumes ]

        self.assertEqual(response.json(), {'result':result})

        self.assertEqual(response.status_code, 200)



               