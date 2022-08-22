from django.db import models
from django.contrib.auth.models import User
import random

class Player(models.Model):
    name = models.TextField(max_length=30)
    score = models.IntegerField()

    def createUser(username):
        entry = Player(name=username, score=random.randint(0,1000000))
        entry.save()

    def getPoints(username):
        users = Player.objects.filter(name=username)
        if len(users)> 1:
            print("MORE THAN ONE USER WITH THAT NAME?!")
        else:
            for user in users:
                score = user.score
                print(score)
            return score

    def addPoints(username, numberOfPoints):
        users = Player.objects.filter(name=username)
        if len(users)> 1:
            print("MORE THAN ONE USER WITH THAT NAME?!")
        else:
            for user in users:
                user.score = user.score + numberOfPoints
                user.save()

    def getLeaderBoard():
        names = []
        scores = []

        def scoreSort(obj):
            return obj.score

        # Get all DB objects and sort by score
        retreivedObjects = Player.objects.all()
        objectList = list(retreivedObjects)
        objectList.sort(reverse = True, key = scoreSort)

        # # Put scores into list
        # for o in objectList:
        #     n = o.name
        #     s = o.score
        #     names.append(n)
        #     scores.append(s)

        return objectList
