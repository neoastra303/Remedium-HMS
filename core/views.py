from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

# Create your views here.
