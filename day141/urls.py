"""day141 URL Configuration

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
from app01 import  views
from app02 import views as app02_view
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^auth/', views.AuthView.as_view()),  # as_view() 就会调用 dispatch()
    # url(r'^hosts/',views.HostView.as_view()),
    # url(r'^user/',views.UserView.as_view()),
    # url(r'^salary/',views.SalaryView.as_view()),
    url(r'^index/',app02_view.IndexView.as_view()),
    url(r'^Manage_index/',app02_view.ManageView.as_view()),
]

