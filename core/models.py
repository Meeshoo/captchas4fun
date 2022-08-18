from django.db import models
from django.contrib.auth.models import User

class core(models.Model):

    def getNumberOfDoughnuts():

        var = "Data"

        try:
            return var
        except:
            print ("No set called")
            return "No data yet"