import boto3, uuid

from django.views import View
from django.http  import JsonResponse

from utils.login_decorator import  login_decorator
from cv.models   import Resume
from my_settings import SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID

class ResumeUploadView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
    )

    @login_decorator
    def post(self,request):
        try:
            file       = request.FILES['filename']
            file_name  = file.name
            file_uuid  = str(uuid.uuid4())
            file_url   = "https://wantubucket1.s3.ap-northeast-2.amazonaws.com/{}".format(file_uuid) 
            user       = request.user

            self.s3_client.upload_fileobj( 
                file,  
                "wantubucket1", 
                file_uuid,    
                ExtraArgs={         
                    "ContentType": file.content_type   
                }
            )

            Resume.objects.create(name = file_name , file_url = file_url, user = user)
        
        except KeyError:
            return JsonResponse({'message':"Key error"}, status=400)

        return JsonResponse({"message":"upload succeed"}, status=200)

class ResumeDownloadView(View):
    @login_decorator
    def get(self,request,resume_pk):

        url  = Resume.objects.get(id= resume_pk).file_url

        return JsonResponse({"message":url}, status=200)