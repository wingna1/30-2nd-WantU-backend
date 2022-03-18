from django.db import models

from utils.time_stamp_model import TimeStampModel

class User(TimeStampModel):
    kakao_nickname    = models.CharField(max_length=20)
    kakao_email       = models.CharField(max_length=50, unique=True)
    kakao_id          = models.BigIntegerField(unique=True)
    profile_image_url = models.URLField(max_length=1500)

    class Meta:
        db_table = "users"
