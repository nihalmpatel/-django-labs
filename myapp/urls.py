from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'courses', views.courses, name='courses'),
    path(r'login', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'courses/<int:course_id>', views.course_details, name='course_details'),
    path(r'<int:top_no>', views.detail, name='detail'),
]
