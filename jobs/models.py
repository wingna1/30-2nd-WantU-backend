from django.db import models


class JobCategory(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "job_categories"

class JobPosition(models.Model):
    title        = models.CharField(max_length=50)
    content      = models.TextField
    due_date     = models.DateField()
    job_category = models.ForeignKey("JobCategory", on_delete=models.CASCADE)
    company      = models.ForeignKey("Company", on_delete=models.CASCADE)

    class Meta:
        db_table = "job_positions"

class Tag(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = "tags"

class TagNotification(models.Model):
    tag          = models.ForeignKey("Tag", on_delete=models.CASCADE)
    job_position = models.ForeignKey("JobPosition", on_delete=models.CASCADE)

    class Meta:
        db_table = "tag_notifications"

class Company(models.Model):
    name             = models.CharField(max_length=30)
    location         = models.CharField(max_length=100)
    average_salary   = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        db_table = "companies"

class CompanyImage(models.Model):
    image_url = models.URLField(max_length=1500)
    company   = models.ForeignKey("Company", on_delete=models.CASCADE)

    class Meta:
        db_table = "company_images"
