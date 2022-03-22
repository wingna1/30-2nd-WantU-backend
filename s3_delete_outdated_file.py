import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wantu.settings")

import django
django.setup()

import datetime

import boto3

from cv.models   import Resume
from my_settings  import SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID

def delete_outdated_file():
    delete_point    = datetime.datetime.now() - datetime.timedelta(days=31) 
    filtered_resume = Resume.objects.filter(is_deleted=True, deleted_at__lte=delete_point)

    for resume in filtered_resume:
        boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
        ).delete_object(Bucket="wantubucket1", Key=str(resume.uuid))

if __name__ == '__main__':
    delete_outdated_file()

