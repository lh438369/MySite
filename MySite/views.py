from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
import json
import random
from blog.models import UserInfo

def login(request):
    login_response={"username":None,"error_msg":None}
    if request.is_ajax():
        username=request.GET.get("username")
        password = request.GET.get("password")
        valid=request.GET.get("valid")
        print(type(valid))
        print(valid)
        session_valid=request.session.get("valid_code")
        print(type(session_valid))
        print(session_valid)
        if valid == session_valid:
            user=auth.authenticate(request,username=username,password=password)
            if user:
                login_response["username"]=username
                request.session["is_login"]=True
            else:
                login_response["error_msg"]="用户名或密码错误，请重新输入"

        else:
            login_response["error_msg"]="验证码错误，请重新输入"
        return HttpResponse(json.dumps(login_response))

    return render(request,"login.html")

def get_image(request):
    from io import BytesIO
    f=BytesIO()
    from PIL import Image,ImageDraw,ImageFont
    img=Image.new(mode='RGB',size=(120,30),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw=ImageDraw.Draw(img,mode='RGB')
    char_list=[]
    for i in range(5):
        char=random.choice([chr(random.randint(65,90)),chr(random.randint(97,122)),str(random.randint(1,9))])
        font=ImageFont.truetype("MySite/static/font/segoesc",24)
        draw.text([i*24,-7],char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        char_list.append(char)
    img.save(f,"png")
    data=f.getvalue()
    s=''.join(char_list)
    request.session["valid_code"]=s
    return HttpResponse(data)

def index(request):
    if request.session.get("is_login"):
        return HttpResponse("index")
    return redirect("/login/")

def login_out(request):
    request.session.flush()
    return redirect("/login/")

from function.myforms import RegiForm
def regi(request):
    if request.is_ajax():
        regiform = RegiForm(request.POST)
        regiResponse={"user":None,"error_msg":None}
        if regiform.is_valid():
            name=regiform.cleaned_data.get("name")
            pwd = regiform.cleaned_data.get("pwd")
            repwd = regiform.cleaned_data.get("repwd")
            email = regiform.cleaned_data.get("email")
            phone = regiform.cleaned_data.get("phone")
            avatar=request.FILES.get("avatar")
            print(avatar)
            print(type(avatar))
            user=UserInfo.objects.create_user(username=name,password=pwd,email=email,telephone=phone,avatar=avatar)
            regiResponse["user"]=user.username
        else:
            regiResponse["error_msg"]=regiform.errors
        return HttpResponse(json.dumps(regiResponse))
    regiform = RegiForm()
    return render(request,"regi.html",{"regiform":regiform})