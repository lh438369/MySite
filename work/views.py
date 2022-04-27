from django.shortcuts import render

# Create your views here.
def work_index(request):
    return render(request,"work_index.html")