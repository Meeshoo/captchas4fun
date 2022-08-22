from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Player
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

@csrf_exempt
def index(request):

    if request.method == 'GET':

        username = None
        if request.user.is_authenticated():
            username = request.user.get_username()

            return TemplateResponse(request, 'fun.html', {"user": username})

@csrf_exempt
def login(request):

    if request.method == 'GET':

        return TemplateResponse(request, 'login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usernameLower = username.lower()


        if User.objects.filter(email=usernameLower).exists():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                try:
                    auth.login(request, user)
                    return TemplateResponse(request, 'fun.html', {"message": "Logged back in!", "username": username, "score": "{:,}".format(Player.getPoints(username))})
                except:
                    print("Didnae work")
                    return TemplateResponse(request, 'login.html', {"message": "Cannot log in with cookie"})
            else:
                print('Wrong')
                return TemplateResponse(request, 'login.html', {"message": "Account exists and password is wrong"})
        else:
            # Uses email field as lower case user check bodge
            user = User.objects.create_user(username=username, password=password, email=usernameLower)
            user.save()

            Player.createUser(username=username)
            
            return TemplateResponse(request, 'fun.html', {"message": "Account created!", "username": username, "score": "{:,}".format(Player.getPoints(username))})
            
def logout(request):
    auth.logout(request)
    return TemplateResponse(request, 'login.html')
