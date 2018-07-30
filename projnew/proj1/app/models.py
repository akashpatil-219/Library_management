# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime,timedelta
# Create your models here.
user_type_CHOICES=[('student','Student'),('librarian','Librarian')]
class Users(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,blank=False)
    password=models.CharField(max_length=50,blank=False)
    email=models.CharField(max_length=50)
    user_type=models.CharField(max_length=50,choices=user_type_CHOICES)
    def __str__(self):
        return self.username +" "+self.user_type

class Books(models.Model):
    title=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    category=models.CharField(max_length=50)
    copies=models.IntegerField(default=0)
    summarry=models.CharField(max_length=500,default="some book")
    def __str__(self):
        return self.title +" "+self.author+" "+self.category


class bookings(models.Model):
    book_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    book_id=models.IntegerField()
    name=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default='Pick up')
    issue_date=models.DateField(default=datetime.today())
    return_date=models.DateField(default=datetime.today())
    def __str__(self):
        return str(self.book_name)+" "+str(self.username)
