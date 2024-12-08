from django.db import models

class User(models.Model):
    mail =  models.EmailField(max_length=100, unique= True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

