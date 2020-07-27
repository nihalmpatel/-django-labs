from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Course
from .forms import OrderForm, InterestForm

# Create your views here.

def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    for top in top_list:
        print(top.id)
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    return render(request, "myapp/about0.html")


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
                        detail.interested = detail.interested+1
                        detail.save()
                    return redirect('myapp:index')
            else:
                interestForm= InterestForm()
                return render(request, 'myapp/course_details.html', {'interestForm': interestForm, 'detail': detail})
       else:
            return redirect('myapp:courses')
   except Course.DoesNotExist:
       return redirect('myapp:courses')
