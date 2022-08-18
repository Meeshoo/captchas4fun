from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import core
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

@csrf_exempt
def index(request):

    if request.method == 'GET':

        return TemplateResponse(request, 'index.html')

@csrf_exempt
def login(request):

    if request.method == 'GET':

        return TemplateResponse(request, 'login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                try:
                    auth.login(request, user)
                    return TemplateResponse(request, 'fun.html', {"message": "Logged back in"})
                except:
                    print("Didnae work")
                    return TemplateResponse(request, 'login.html', {"message": "Cannot log in with cookie"})
            else:
                print('no user')
                return TemplateResponse(request, 'login.html', {"message": "Account exists and password is wrong"})
        else:
            user = User.objects.create_user(username=username, password=password, )
            user.save()
            
            return TemplateResponse(request, 'fun.html', {"message": "Account created!"})
            
def logout(request):
    auth.logout(request)
    return TemplateResponse(request, 'login.html')
