from django.db import models

# Create your models here.
class Facility(models.Model):
    facility_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    county = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=16)
    district = models.CharField(null=True, blank=True, max_length=100)
    telephone = models.CharField(null=True, blank=True, max_length=32)
    latest_inspection = models.DateTimeField(null=True, blank=True)

class Checklist(models.Model):
    checklist_name = models.CharField(max_length=200)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)

    released_to_environment = models.BooleanField()
    residue = models.BooleanField()
    burned = models.BooleanField()
    records_of_volume = models.BooleanField()
    disposal = models.BooleanField()
    recyclable_materials = models.BooleanField()
    recycled_on_site = models.BooleanField()

class Letters(models.Model):
    letter_subject = models.CharField(max_length=200)
    content = models.CharField(max_length=800)
    date_modified = models.DateTimeField(auto_now=True)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
