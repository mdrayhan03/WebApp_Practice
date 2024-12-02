from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from . import customlogin
from supabasedb import supabase

# Create your views here.
def langpage(request) :
    return render (request, "baseapp/landpage.html")

def gmail_login(request) :
    gm = customlogin.Gmail_login()
    info = gm.authenticate_with_google()        
    info = {
        "email" : info["email"],
        "name" : "name"
    }
    request.session["info"] = info
    return redirect('baseapp:login')

def gmail_ca(request) :
    gm = customlogin.Gmail_login()
    info = gm.authenticate_with_google()
    info = {
        "email" : info["email"],
        "name" : info["name"],
    }
    request.session["info"] = info
    return redirect('baseapp:create_account')

def facebook_login(request) :
    fb = customlogin.Facebook_login()
    info = fb.work()

    request.session["info"] = info
    return redirect('baseapp:login')

def facebook_ca(request) :
    fb = customlogin.Facebook_login()
    info = fb.work()   

    request.session["info"] = info
    return redirect('baseapp:create_account')

@csrf_exempt
def login(request) :
    if request.COOKIES.get("remember_me") == "true":
        return redirect("baseapp:homepage")    

    if request.method == "POST" :
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        value = request.POST.get("action")

        supa = supabase.Supabase()
        response = supa.login_account(email, password)

        if response == False :
            messages.error(request, "Login unsuccessful.")
            return redirect("baseapp:login")
       
        button = request.POST.get("submit_btn")
        if button == "submit" :            
            response = redirect("baseapp:homepage")
            if remember_me == "on" :
                response.set_cookie("remember_me", "true", max_age=31536000, samesite='Lax', secure=False)
            return response
    
    info = request.session.get("info")
    
    return render(request, "baseapp/login.html", info)

def create_account(request) :
    info = request.session.get("info")

    if request.method == "POST" :
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        supa = supabase.Supabase()
        response = supa.create_account(name, email, password)        
        
    return render(request, "baseapp/createAcc.html", info)

def logout(request) :
    if "info" in request.session :
        del request.session["info"]
    response = redirect("baseapp:login")
    response.delete_cookie("remember_me")
    

    return response

def homepage(request) :
    # if request.COOKIES.get("remember_me") == "true":
    return render(request, "baseapp/homepage.html")
    
    # return redirect("baseapp:login")

def profile(request) :
    return render(request, "baseapp/profile.html")