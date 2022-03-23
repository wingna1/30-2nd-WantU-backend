import json

from enum                   import Enum

from django.views           import View
from django.core.exceptions import MultipleObjectsReturned
from django.http            import JsonResponse, HttpResponse
from django.db.models       import Q

from utils.login_decorator import  login_decorator
from users.models          import User
from applications.models   import Applicant,ApplicationStatus,Application
from cv.models             import Resume
from jobs.models           import JobPosition  

class Status(Enum): 
    APPLIED         = 1
    DOCUMENT_PASSED = 2
    ACCEPTED        = 3
    REJECTION       = 4

class StatusView(View):
    @login_decorator
    def get(self, request):
        applicant = Applicant.objects.filter(user=request.user).prefetch_related('application_set')

        if not applicant.exists():
            return JsonResponse({'result':"NO valid application"}, status = 404)

        applications_in_applicant = applicant[0].application_set.all().select_related('status')          
        status_list               = [application.status.id for application in applications_in_applicant]

        result = { 
            "applied"         : status_list.count(Status.APPLIED.value), 
            "document_passed" : status_list.count(Status.DOCUMENT_PASSED.value),
            "accepted"        : status_list.count(Status.ACCEPTED.value),
            "rejection"       : status_list.count(Status.REJECTION.value)
            }

        result["total"] = len(status_list)

        return JsonResponse({'result':result}, status = 200) 
    

class CompanyView(View):        
    @login_decorator
    def get(self, request, status):
        applicant = Applicant.objects.filter(user=request.user).prefetch_related('application_set')

        if not applicant.exists():
            return JsonResponse({'result':None}, status = 404)

        q = Q()
        
        status_list = {
            'applied'        : Q(status__status='applied'),
            'document_passed': Q(status__status='document_passed'),
            'accepted'       : Q(status__status='accepted'),
            'rejection'      : Q(status__status='rejection'),
            'all'            : Q()
        }

        
        q.add(status_list[status],Q.AND)

        qualified_applications = applicant[0].application_set.all().filter(q).select_related('job_position')

        result = [{
            "company_name" : application.job_position.company.name,
            "category"     : application.job_position.job_category.name,
            "applied_date" : application.created_at.strftime('%Y.%m.%d'),
            "apply_status" : application.status.status
        }for application in qualified_applications]

        return JsonResponse({'result':result}, status=200)


        
class ApplyView(View):       
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try: 
            applicant, created = Applicant.objects.get_or_create(user = request.user)

            Application.objects.create(
                applicant    = applicant,
                resume       = Resume.objects.get(uuid=data["uuid"]),
                job_position = JobPosition.objects.get(id=data["job_position_id"]), 
                status       = ApplicationStatus.objects.get(id=Status.APPLIED.value) 
                )

            return JsonResponse({"message":"Successfully Applied"}, status=201)

        except Applicant.MultipleObjectsReturned:
            return JsonResponse({'message': "Multiple objects returned, please check applicant or databases!"})

