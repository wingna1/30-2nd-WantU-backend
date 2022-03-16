from django.db import models

from utils.time_stamp_model import TimeStampModel
from users.models           import User

class Resume(TimeStampModel):
    name     = models.CharField(max_length=30)
    file_url = models.URLField(max_length=1500)
    user     = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta:
        db_table = "resumes"
