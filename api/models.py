from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    email = models.EmailField()
    age = models.IntegerField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.second_name


class MembershipType(models.Model):
    interval_start = models.TimeField()
    interval_end = models.TimeField()

    interval_end = models.TimeField()