from functools import reduce
from django.http import Http404
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.conf import settings
from .models import Player
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
import requests
import json

@csrf_exempt
def play(request):

    if request.method == 'GET':

        username = None
        if request.user.is_authenticated:
            username = request.user.username
            return TemplateResponse(request, 'fun.html', {"message": "", "username": username, "score": "{:,}".format(Player.getPoints(username))})

        else:
            return TemplateResponse(request, 'login.html', {"message": "You were logged out, likely a cookie thing"})

    if request.method == 'POST':
        username = request.user.username
        captchaResult = request.POST['g-recaptcha-response']
        postData = {   
            "secret" :settings.CAPTCHA_SECRET,
            "response" : captchaResult,
        }   
        r = requests.post(' https://www.google.com/recaptcha/api/siteverify', params=postData)
        captchaResponse = json.loads(r.text)
        print(captchaResponse)
        if captchaResponse['success']:
            Player.addPoints(username, 50)
            return TemplateResponse(request, 'fun.html', {"message": "CAPTCHA complete! +50 points!", "username": username, "score": "{:,}".format(Player.getPoints(username))})
        else:
            return TemplateResponse(request, 'fun.html', {"message": "CAPTCHA failed", "username": username, "score": "{:,}".format(Player.getPoints(username))})

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
                    return redirect(play)
                except:
                    print("Didnae work")
                    return TemplateResponse(request, 'login.html', {"message": "Cannot log in with cookie"})
            else:
                print('Wrong')
                return TemplateResponse(request, 'login.html', {"message": "Account exists and password is wrong"})
        else:
            if not username.isalnum():
                return TemplateResponse(request, 'login.html', {"message": "Username must only contain letters and numbers"})

            elif len(password) < 3:
                return TemplateResponse(request, 'login.html', {"message": "Password must be 3 characters or longer"})

            else:
                # Uses email field as lower case user check bodge
                user = User.objects.create_user(username=username, password=password, email=usernameLower)
                user.save()

                auth.login(request, user)

                Player.createUser(username=username)
                
                return redirect(play)
                
            
def logout(request):
    auth.logout(request)
    return TemplateResponse(request, 'login.html')

def leaderboard(request):
    data = Player.getLeaderBoard()
    return TemplateResponse(request, 'leaderboard.html', {"data": data})
