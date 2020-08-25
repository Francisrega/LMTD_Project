from django.shortcuts import render
from FoodieBlog.models import Student

def index(request):

    if request.method == 'POST':
        fname = request.POST.get('fname')
        email = request.POST.get('email')

        s = Student(firstname=fname, email=email)
        s.save()
    return render(request, 'FoodieBlog/index3.html')

# def indexes(request):
#
#     if request.method == 'POST':
#         fname = request.POST.get('fname')
#         email = request.POST.get('email')
#
#         s = Student(firstname=fname, email=email)
#         s.save()
#     return render(request, 'FoodieBlog/index2.html')

