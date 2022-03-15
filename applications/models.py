from django.db import models

from utils.time_stamp_model import TimeStampModel
from users.models           import User
from cv.models              import Resume
from jobs.models            import JobPosition


class Applicant(TimeStampModel):
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta:
        db_table = "applicants"

class ApplicationStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "application_status"

class Application(TimeStampModel):
    applicant    = models.ForeignKey("Applicant", on_delete=models.CASCADE)
    resume       = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    status       = models.ForeignKey("ApplicationStatus", on_delete=models.CASCADE)

    class Meta:
        db_table = "applications"
