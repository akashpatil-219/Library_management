# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from app.models import Users,Books,bookings
from django.db.models import Q
import models
from datetime import datetime,timedelta
from reportlab.pdfgen import canvas
from django.http import HttpResponse

# Create your views here.
@csrf_exempt
def register(request):
    #print request.method
    if(request.method=="POST"):
        context={}
        name=request.POST['name']
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        user_type=request.POST['user_type']
        context['name']=name
        context['username']=username
        context['password']=password
        context['email']=email
        context['user_type']=user_type
        if Users.objects.filter(username=context['username']).exists():
            context['message']="username already exist"
            httpresponse=render(request,'reg.html',context)
            return httpresponse
        else:
            obj=Users(name=context['name'],username=context['username'],password=context['password'],email=context['email'],user_type=context['user_type'])
            obj.save()
            return redirect('/login')
    else:
         httpresponse=render(request,'reg.html',{})
         return httpresponse



#pseudocode for login:
#take input
#check if username exists and the corresponding password if valid.
#if valid check the type of the username
# if user=student :redirect to student
#else user=librarian :redirect to librarian dashborad
@csrf_exempt
def login(request):
    if ('username' in request.session):
        username = request.session['username']
        user_type=request.session['user_type']
        if(user_type=="student"):
            return redirect('/student_dashboard')
        else:
            return redirect('/librarian_dashboard')
    if(request.method=="POST"):
        context={}
        context['username']=request.POST['username']
        context['password']=request.POST['password']
        if Users.objects.filter(username=context['username']).exists():
            if Users.objects.filter(username=context['username'],password=context['password']).exists():
                user_objects=Users.objects.get(username=context['username'],password=context['password'])
                if(user_objects.user_type=="librarian"):
                    request.session['username']=user_objects.username
                    request.session['user_type']=user_objects.user_type
                    return redirect('/librarian_dashboard')
                elif(user_objects.user_type=="student"):
                    request.session['username']=user_objects.username
                    request.session['user_type']=user_objects.user_type
                    return redirect('/student_dashboard')
                else:
                    context['message']="wrong password"
                    httpresponse=render(request,'login.html',context)
                    return httpresponse
        else:
            context['message']="user does not exist"
            httpresponse=render(request,'login.html',context)
            return httpresponse
    else:
        httpresponse=render(request,'login.html',{})
        return httpresponse
@csrf_exempt
def student_dashboard(request):
    if ('username' in request.session):
        books=list(Books.objects.all())
        context={}
        context['username']=request.session['username']
        context['Books']=books
        context['bookings'] = models.bookings.objects.filter(username=request.session['username'])
        print context['bookings']
        return render(request,'student_dashboard.html',context)
    else:
        return redirect('/login')


@csrf_exempt
def librarian_dashboard(request):
    if('user_type' in request.session):
        if(request.session['user_type']=='librarian'):
            context={}
            obj_user=models.Users.objects.get(username=request.session['username'])
            context['username']=obj_user.username
            context['name']=obj_user.name
            context['user_type']=obj_user.user_type
            context['books'] = list(models.Books.objects.all())
            context['bookings'] = list(models.bookings.objects.all())
            context['returns']=list(models.bookings.objects.filter(return_date = datetime.today()))

            context['message1']="Librarian"
            response=render(request,"librarian_dashboard.html",context)

            return response
    else:
        context['message']="Invalid credentials"
        return redirect("/login",context)



@csrf_exempt
def logout(request):
    if ('username' in request.session):
        del request.session['username']
        del request.session['user_type']
        return redirect('/login')
    else:
        return redirect('/login')
@csrf_exempt
def book_details(request):
    id1=request.GET["book_id"]
    book_objects=Books.objects.get(id=id1)
    context={}
    summ=book_objects.summarry
    context['message']=summ
    httpresponse=render(request,'book_details.html',context)
    return httpresponse


@csrf_exempt
def add_books(request):
	if request.method=='POST':
		if request.POST['Name']!="":
			Name = request.POST['title']
			Author = request.POST['Author']
			no_of_copies = request.POST['copies']
			subject = request.POST['subject']
			summary = request.POST['summary']
			context = {}
			if models.Books.objects.filter(title=Name,author = Author,category = subject).exists():
				obj_user = models.Books.objects.get(name = Name,author = Author,subject = subject)
				tot_book = int(obj_user.copies)
				tot_book = tot_book + int(no_of_copies)
				models.Books.objects.get(title = Name,author = Author,category = subject).delete()
				obj_user.copies = str(tot_book)
				obj = models.Books(
				title = obj_user.title,
				author = obj_user.author,
				copies = obj_user.copies,
				category = obj_user.category,
				summarry = obj_user.summarry,
				)
				obj.save()
			else:
				obj = models.Books(
				title = Name,
				author = Author,
				copies = no_of_copies,
				category = subject,
				summarry = summary,
				)
				obj.save()
			response = redirect('/librarian_dashboard')
		else:
			context = {}
			context['message'] = "Invalid entry"
    			response = render(request,"add_books.html",context)
	else:
		response = render(request,'add_books.html',{})
	return response


@csrf_exempt
def stud_profile(request):
    context={}
    username = request.session['username']
    user_type=request.session['user_type']
    studobj=Users.objects.get(username=request.session['username'])
    context['username']=studobj.username
    context['name']=studobj.name
    context['user_type']=studobj.user_type
    context['email']=studobj.email
    httpresponse=render(request,'student_profile.html',context)
    return httpresponse

@csrf_exempt
def search_books(request):
    title1=request.POST['title']
    author1=request.POST['author']
    category1=request.POST['category']
    context={}
    book_objects=Books.objects.filter(Q(title=title1) | Q(author=author1) |Q(category=category1))
    context['m']=book_objects
    httpresponse=render(request,'search_result.html',context)
    return httpresponse
@csrf_exempt
def session_check(request):
        if ('username' in request.session):
            user_type=request.session['user_type']
            if(user_type=="student"):
                return redirect('/student_dashboard')
            else:
                return redirect('/librarian_dashboard')
        else:
            return redirect('/login')


@csrf_exempt
def book_a_book(request):
    context={}
    context['username']=request.GET['username']
    context['book_id']=request.GET['book_id']
    obj_user_student=models.Users.objects.get(username=context['username'])

    bookings_till_now = models.bookings.objects.filter(username=context['username']) & (models.bookings.objects.filter(status ='Pick up')|models.bookings.objects.filter(status ='To be Returned'))

    if(len(bookings_till_now)>1):
        context['flag']='Unsuccessful \n Cant Issue more than 2 books'
        return render(request,"booking_summary.html",context)

    for i in bookings_till_now:
        if(str(i.book_id)==str(context['book_id'])):
            context['flag']='Unsuccessful \n Cant Issue Same book more than 1 time'
            return render(request,"booking_summary.html",context)

    obj_user = models.Books.objects.get(id=context['book_id'])
    tot_book = int(obj_user.copies)

    if(tot_book>0):
        tot_book=tot_book-1

        obj_user.copies = str(tot_book)
        obj_user.save(update_fields=['copies'])

        obj2 = models.bookings(
        book_name=obj_user.title,
        username=str(context['username']),
        book_id=str(context['book_id']),
        name=obj_user_student.name,
        )
        obj2.save()

        context['flag']='Successful'
    else:
        context['flag']='Unsuccessful \nInsufficient books'

    return render(request,"booking_summary.html",context)

def approve(request):
    obj=models.bookings.objects.get(id=request.GET['booking_id'])
    if(obj.status=='Pick up'):
        obj.status='To be Returned'

    elif(obj.status=='To be Returned'):
        obj.status='Returned'
        book_obj=models.Books.objects.get(id=request.GET['book_id'])
        book_obj.copies=str(int(book_obj.copies)+1)
        book_obj.save(update_fields=['copies'])
        ret_date=datetime.today().date()
        expected_return_date=obj.return_date
        print "hi"
        print obj.return_date
        print "hi"
        delay=(ret_date-expected_return_date).days
        if(delay>0):
            fine=50*delay
        else:
            fine=0
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment';
        filename="somefilename.pdf"
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

    obj.save(update_fields=['status'])
    return redirect("/librarian_dashboard")
### raise http 404
