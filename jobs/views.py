from django.http            import JsonResponse
from django.db.models       import Q
from django.views           import View
from django.core.exceptions import FieldError

from applications.models    import Applicant, Application
from jobs.models            import JobPosition
from utils.login_decorator  import login_decorator

class JobPositionUserDataView(View):
    @login_decorator
    def get(self, request, job_position_id):
        user        = request.user
        application = False

        if Applicant.objects.filter(user_id=user.id):
            application = Application.objects.filter(applicant_id=user.applicant_set.first().id, job_position_id=job_position_id)

        is_applied = True if application else False
        resumes    = [{
                "name"        :resume.name,
                "created_date":resume.created_at.strftime("%Y.%m.%d"),
                "uuid"        :resume.uuid
            } for resume in user.resume_set.all().filter(is_deleted=False)]

        user_data = { 
            "is_applied"    :is_applied,
            "kakao_email"   :user.kakao_email,
            "kakao_nickname":user.kakao_nickname,
            "resumes"       :resumes
        }
        return JsonResponse({"results":user_data}, status=200)
        
class JobPositionDetailView(View):
    def get(self, request, job_position_id):
        try:
            job_position = JobPosition.objects.get(id=job_position_id)

            company = job_position.company

            tag_list = job_position.tagnotification_set.all()
            tags     = [ tag.tag.name for tag in tag_list ]

            image_list = job_position.company.companyimage_set.all()
            images     = [ image.image_url for image in image_list ]

            data = {   
                    "job_position_id"       :job_position.id,
                    "job_categories_name"   :job_position.job_category.name,
                    "due_date"              :job_position.due_date,
                    "title"                 :job_position.title,
                    "content"               :job_position.content,
                    "company_name"          :company.name,
                    "company_location"      :company.location,
                    "company_average_salary":company.average_salary,
                    "tags"                  :tags,
                    "images"                :images
            }
            return JsonResponse({"results":data}, status=200)
        except JobPosition.DoesNotExist:
            return JsonResponse({"message":"Data Does Not Exist"}, status=400) 

class JobPositionListView(View):
    def get(self, request):
        try:
            tag_id      = int(request.GET.get("tag", 0))
            category_id = int(request.GET.get("category", 0))
            location    = request.GET.get("area")
            sort        = request.GET.get("sort", "id")
            offset      = int(request.GET.get("offset", 0))
            limit       = int(request.GET.get("limit", 8))

            q = Q()
            if category_id != 0:
                q &= Q(job_category_id=category_id)
            if tag_id != 0:
                q &= Q(tagnotification__tag_id=tag_id)    
            if location:
                q &= Q(company__location__startswith=location)
            
            requested_queryset = JobPosition.objects.select_related("company").filter(q).order_by(sort)
            sliced_queryset    = requested_queryset[offset:limit]

            list_data = [{
                "job_position_id"  : data.id,
                "title"            : data.title,
                "company_name"     : data.company.name,
                "company_location" : data.company.location,
                "company_image"    : data.company.companyimage_set.first().image_url
            } for data in sliced_queryset]

            results = {
                "total_count" : len(requested_queryset),
                "list_data"   : list_data
                }

            return JsonResponse({"results":results}, status=200)
        except KeyError:
            return JsonResponse({"message":"Invalid Parameter"}, status=400) 
        except ValueError:
            return JsonResponse({"message":"Invalid Type of Parameter"}, status=400) 
        except FieldError:
            return JsonResponse({"message":"Invalid Type of Parameter"}, status=400) 
