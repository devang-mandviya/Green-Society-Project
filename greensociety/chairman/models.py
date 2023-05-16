from email.policy import default
from enum import auto,unique
from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    otp = models.IntegerField(default=229)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.email

class Chairman(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=30,blank=True,null=True)
    lastname = models.CharField(max_length=30,blank=True,null=True)
    contact = models.CharField(max_length=15,blank=True,null=True)
    gender = models.CharField(max_length=30,blank=True,null=True)
    visting_time = models.CharField(max_length=20,blank=True,null=True)
    pic = models.FileField(upload_to = 'media/images/',default='media/person.png')
    
    def __str__(self) -> str:
        return self.firstname + " " +self.lastname 


class Member(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    gender = models.CharField(max_length=30,blank=True,null=True)
    house_no = models.CharField(max_length=10,blank=True,null=True)
    occupation = models.CharField(max_length=40,blank=True,null=True)
    working_place = models.CharField(max_length=30,blank=True,null=True)
    family_mambers = models.CharField(max_length=10,blank=True,null=True)
    vehicale_details = models.CharField(max_length=30,blank=True,null=True)
    birthdate = models.DateField (blank=True,null=True)
    pic = models.FileField(upload_to = 'media/images/',default='media/person.png')
    
    def __str__(self) -> str:
        return self.firstname + " " +self.lastname 


class Notice(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length=500,blank=True,null=True)
    pic = models.FileField(upload_to = 'media/images/',default='media/default.png')
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self) -> str:
        return self.title

class Event(models.Model):
    user_id = models.ForeignKey(User,on_delete= models.CASCADE)
    title = models.CharField(max_length=50,blank=True,null=True)
    description = models.TextField(max_length=50,blank=True,null=True)
    date_event = models.DateField(blank=True,null=True)
    event_time = models.TimeField(blank=True,null=True)
    pic = models.FileField(upload_to = "media/images/",default='media/default.png')

    def __str__(self) -> str:
        return self.title
    
class Post(models.Model):
    user_id = models.ForeignKey(User,on_delete= models.CASCADE)
    name = models.CharField (max_length=30)
    product = models.CharField(max_length=15,blank=True,null=True)
    option = models.CharField (max_length=10,blank=True,null=True)
    contact = models.CharField (max_length=12,blank=True,null=True)
    price = models.CharField (max_length=10,blank=True,null=True)
    pic = models.FileField (upload_to = 'media/images/',default='media/default.png')

    def __str__(self) -> str:
        return self.name 
    
class Maintainance (models.Model):
    user_id = models.ForeignKey(User,on_delete= models.CASCADE)
    member_id = models.ForeignKey(Member,on_delete= models.CASCADE)
    title = models.CharField (max_length=30)
    amount = models.CharField(max_length=30)
    duedate = models.DateField (blank=True,null=True)
    status = models.CharField (max_length=20,default="PENDING")