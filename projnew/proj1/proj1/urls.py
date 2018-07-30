"""proj1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reg/', views.register),
    url(r'^login/',views.login),
    url(r'^student_dashboard/',views.student_dashboard),
    url(r'^librarian_dashboard/',views.librarian_dashboard),
    url(r'^logout/',views.logout),
    url(r'^book_details/',views.book_details),
    url(r'^student_profile/',views.stud_profile),
    url(r'^add_books/',views.add_books),
    url(r'^book_details/',views.book_details),
    url(r'^book_a_book/',views.book_a_book),
    #url(r'^approve/',views.approve),
    #url(r'^$',views.session_check),

]
