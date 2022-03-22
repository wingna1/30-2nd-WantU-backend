import boto3, uuid, json

from django.utils import timezone
from django.views import View
from django.http  import JsonResponse, HttpResponse

from utils.login_decorator  import  login_decorator
from cv.models              import Resume
from my_settings            import SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID

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

            Resume.objects.create(name = file_name , file_url = file_url, uuid= file_uuid, user = user )
        
        except KeyError:
            return JsonResponse({'message':"Key error"}, status=400)

        return JsonResponse({"message":"upload success"}, status=201)

class ResumeInfoView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
        )

    @login_decorator
    def get(self,request,resume_pk):
        try:    
            url  = Resume.objects.get(uuid= resume_pk).file_url

            return JsonResponse({"message":url}, status=200)

        except Resume.DoesNotExist:
            return JsonResponse({'message':"Invalid resume_pk"}, status=404)

    @login_decorator
    def post(self,request,resume_pk): 
        try:
            data = json.loads(request.body) 
            file_name = data["name"]

            resume = Resume.objects.filter(uuid=resume_pk)

            if resume.exists() :
                resume.update(name=file_name)
                return HttpResponse(status=201) 
            
            else:
                return JsonResponse({'message': 'Invalid resume_pk'}, status=404)

        except KeyError:
            return JsonResponse({'message':'Key Error'}, status=400)

    @login_decorator
    def delete(self,request,resume_pk):
        resume = Resume.objects.filter(uuid=resume_pk)

        if resume.exists():
            
            resume.update(is_deleted=True, deleted_at=timezone.now())

            return HttpResponse(status=200)

        else:
            return JsonResponse({'message': 'Invalid resume_pk'}, status=404) 

class ResumeListView(View):
    @login_decorator
    def get(self,request):

        results = [{
            "uuid"         : resume.uuid,
            "name"         :resume.name,
            "created_date" : resume.created_at.strftime('%Y.%m.%d')
        } for resume in Resume.objects.filter(user=request.user).exclude(is_deleted=True)] 

        return JsonResponse({"result": results}, status=200)