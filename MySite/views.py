from django.shortcuts import render,HttpResponse,redirect

def index(request):
    return render(request,"index.html")

def login_html(request):
    return render(request,"login.html")

def login(request):
    user=request.POST.get("user")
    pwd=request.POST.get("pwd")
    loginResponse={"user":None,"errorMsg":None}
    if user=="lihu" and pwd=="123":
        loginResponse["user"]="lihu"
    else:
        loginResponse["errorMsg"]="用户名或密码错误"
    import json
    return HttpResponse(json.dumps(loginResponse))


from django import forms
from django.forms import widgets
class RegiForm(forms.Form):
    username=forms.CharField(min_length=8)
    password=forms.CharField(
        widget=widgets.PasswordInput()
    )
    repeat_password=forms.CharField(
        widget=widgets.PasswordInput()
    )
    phone=forms.IntegerField()
    email=forms.EmailField()

def regi(request):
    if request.method=="POST":
        regiform=RegiForm(request.POST)
        if regiform.is_valid():
            print(regiform.cleaned_data)
        else:
            print(regiform.errors)
        return render(request,"regi.html",{"regiform":regiform})
    regiform=RegiForm()
    return render(request,"regi.html",{"regiform":regiform})