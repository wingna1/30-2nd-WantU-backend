import uuid

from django.db import models
from datetime import datetime

from utils.time_stamp_model import TimeStampModel
from users.models           import User

class Resume(TimeStampModel):
    name       = models.CharField(max_length=30)
    file_url   = models.URLField(max_length=1500)
    uuid       = models.UUIDField(primary_key=False , default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete= models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "resumes"
