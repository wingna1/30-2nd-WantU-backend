from django.db import models

from utils.time_stamp_model import TimeStampModel

class User(TimeStampModel):
    name                = models.CharField(max_length=20)
    kakao_id            = models.BigIntegerField(unique=True)
    profile_image_url   = models.URLField(max_length=200)

    class Meta:
        db_table = "users"
