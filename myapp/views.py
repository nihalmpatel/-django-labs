from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Topic, Course, Student, Order
from .forms import OrderForm, InterestForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


# Create your views here.

def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    for top in top_list:
        print(top.id)
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    views = 0
    if 'about_visits' in request.session:
        views = int(request.session.get('about_visits')) + 1
        request.session['about_visits'] = views
        print('Increasing visit..')
    else:
        request.session.__setitem__('about_visits', 1)
        request.session.set_expiry(300)
        print('Creating about_visit cookie..')
    return render(request, "myapp/about0.html", {'visits': views})


def detail(request, top_no):
    topic = get_object_or_404(Topic, pk=top_no)
    courses = Course.objects.filter(topic=topic)

    return render(request, 'myapp/detail0.html', {'topic': topic, 'courses': courses})


def courses(request):
    courlist = Course.objects.all().order_by('id')
    print(courlist)
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            form.save_m2m()
            allCourses = order.courses.filter(price__gt=150)
            if allCourses:
                [orderObj.discount() for orderObj in allCourses]
            msg = 'Your course has been ordered successfully.'
        else:
            msg = 'You exceeded the number of levels for this course.'
        return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})
    # return HttpResponse('<h1>You can place an order here.</h1>')


def course_details(request, course_id):
    try:
        detail = Course.objects.get(pk=course_id)
        if detail:
            if request.method == 'POST':
                form = InterestForm(request.POST)
                if form.is_valid():
                    interestCourse = form.cleaned_data
                    if interestCourse['interested'] == '1':
                        detail.interested = detail.interested + 1
                        detail.save()
                    return redirect('myapp:index')
            else:
                interestForm = InterestForm()
                return render(request, 'myapp/course_details.html', {'interestForm': interestForm, 'detail': detail})
        else:
            return redirect('myapp:courses')
    except Course.DoesNotExist:
        return redirect('myapp:courses')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usr = form.cleaned_data
        username = usr['username']
        password = usr['password']
        u = User.objects.get(username=username)
        user = None
        if password == u.password:
            user = u

        if user:
            if user.is_active:
                if request.session.test_cookie_worked():
                    print('Woohoo! Test Cookie Worked')
                    request.session.delete_test_cookie()
                    request.session['last_login'] = datetime.now().timestamp()
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                else:
                    print('Test Cookie did not work')

                login(request, user)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                print("account disable")
                return HttpResponse('Your account is disabled.')
        else:
            print("login invalid")
            return HttpResponse('Invalid login details.')
    else:
        loginForm = LoginForm()
        print('Setting up a Test Cookie')
        request.session.set_test_cookie()
        return render(request, 'myapp/login.html', {'loginForm': loginForm})


@login_required
def user_logout(request):
    request.session.flush()
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

@login_required
def myaccount(request):
    data = {}
    message = ''
    print(request.user.pk)
    if request.user.is_staff:
        message = 'You are not Registered Student'
    else:
        data['fname'] = request.user.first_name
        data['lname'] = request.user.last_name
        studentTopics = Student.objects.get(pk=request.user.pk)
        print(studentTopics)
        data['topics'] = studentTopics.interested_in.all()
        data['orders'] = studentOrders = Order.objects.filter(student__id=request.user.pk)
        if studentOrders:
            data['courses'] = [order.courses.all() for order in studentOrders]
    return render(request, 'myapp/myaccount.html', {'user_data': data, 'message': message})
