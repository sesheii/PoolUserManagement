from django.db import models


class MembershipType(models.Model):
    interval_start = models.TimeField()
    interval_end = models.TimeField()

    price = models.FloatField()

    def __str__(self):
        return f"Membership Type ({self.pk})"


class User(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)

    email = models.EmailField()
    age = models.IntegerField()

    registration_date = models.DateTimeField(auto_now_add=True)
    membership_types = models.ManyToManyField(MembershipType)

    def __str__(self):
        return self.first_name + ' ' + self.second_name
