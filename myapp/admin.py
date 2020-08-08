from django.contrib import admin
from django.db import models
from django.db.models import F

from .models import Topic, Course, Student, Order

# Register your models here.
admin.site.register(Topic)
admin.site.register(Order)





@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'price', 'hours', 'for_everyone')
    ordering = ('name',)
    actions = ['add_50_to_hours']

    def add_50_to_hours(self, request, queryset):
        queryset.update(hours= F('hours') + 10)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city')
    ordering = ('first_name',)



