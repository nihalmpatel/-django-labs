from django.db import models
import datetime
from django.contrib.auth.models import User
import decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_price(value):
    if value < 100 or value > 200:
        raise ValidationError(
            _('%(value)s is not in the range of 100-200.'),
            params={'value': value},
        )


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(blank=False, max_length=50, default='Development')

    def __str__(self):
        return self.name


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    hours = models.DecimalField(max_digits=3, decimal_places=0,default=0)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name

    def discount(self):
        self.price = self.price * decimal.Decimal(0.9)
        self.save()


class Student(User,models.Model):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    avatar=models.ImageField(upload_to = 'avatars/', default = 'avatars/None/no-img.jpg')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def full_name(self):
        return self.upper_case_name(self.first_name)+" "+self.upper_case_name(self.last_name)

    def upper_case_name(self,name):
        return name.upper()


class Order(models.Model):
    STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    courses = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    order_date = models.DateField(default=datetime.date.today)

    #
    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.student.first_name, self.student.last_name,
                                             self.levels, self.order_status, self.order_date,
                                             self.total_cost(), self.combined_course_names())

    def combined_course_names(self):
        course_names = ''
        for course in self.courses.all():
            course_names += ' - ' + course.name

        return course_names

    def total_cost(self):
        total_cost = 0
        for course in self.courses.all():
            total_cost += course.price
        return total_cost
