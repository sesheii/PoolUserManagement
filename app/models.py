from django.db import models


class MembershipType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.TimeField()
    price = models.FloatField()

    def __str__(self):
        return f'{self.name}; {self.description}; {self.duration}; {self.price} грн'


class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    is_blocked = models.BooleanField()
    memberships = models.ManyToManyField(MembershipType, through='UserMembership')

    def __str__(self):
        return f'{self.full_name}; {self.email}, {"заблокований" if self.full_name else "все ок"}'


class UserMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Підписка користувача: {self.user.full_name} - Тип: {self.membership_type.name}'


class CheckInCheckOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()

    def __str__(self):
        return f'Час входу: {self.check_in_time}, час виходу: {self.check_out_time}'
