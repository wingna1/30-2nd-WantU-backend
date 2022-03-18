import jwt

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import  SimpleUploadedFile
from users.models                   import User
from .models                        import Resume

from my_settings import SECRET_KEY, ALGORITHM

# Create your tests here.
class ResumeUploadView(TestCase):
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

class ResumeDownloadView(TestCase):
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

        cls.resume = Resume.objects.create(
            id       = 1,
            name     = "test",
            file_url = "www.test.com",
            user     = cls.user
        )

    def test_success_download_resume_from_wantu_get(self):
        client   = Client()

        response = client.get('/cv/1',  **self.header)
        
        self.assertEqual(response.json(),{"message":"www.test.com"})

        self.assertEqual(response.status_code, 200)

    def test_fail_download_resume_from_wantu_get_due_to_wrong_resume_pk_None_returned(self):
            client   = Client()

            response = client.get('/cv/500',  **self.header)

            self.assertEqual(response.json(),{'message': 'Invalid resume_pk'})

            self.assertEqual(response.status_code, 404) 



               