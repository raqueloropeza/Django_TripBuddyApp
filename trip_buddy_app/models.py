from django.db import models
from datetime import date, datetime
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors["first_name"] = "First name should be at least 2 characters."
        if len(postData['last_name'])<2:
            errors["last_name"] = "Last name should be at least 2 characters."
        if len(postData['password'])<8:
            errors["email"] = "Password must be at least 8 characters."
        if (postData['confirmpassword'] != postData['password']):
            errors["password"] = "Passwords must match!"

        user = Users.objects.filter(email=postData['email'])
        if user:
            errors["email"] = "Email is already registered. Login with email and password."
         
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Must include a valid email."
        
        return errors

class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['destination'])<3:
            errors["destination"] = "Destination should be at least 3 characters."
        if len(postData['plan'])<3:
            errors["plan"] = "A plan must be provided!"
        if postData['startdate'] == '':
            errors["start date"] = "You must enter a start date."
        return errors
    

class Users(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 64)
        #trips_uploaded= list of trips uploaded by a given user
        #joined_trips= list of trip joined by a given user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trips(models.Model):
    destination = models.CharField(max_length = 45)
    start_date = models.DateField()
    end_date = models.DateField()
    uploaded_by = models.ForeignKey(Users, related_name="trips_uploaded", on_delete = models.CASCADE)
        #user who created trip
    users_who_joined = models.ManyToManyField(Users, related_name="joined_trips")
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
