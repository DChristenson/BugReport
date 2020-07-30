"""bugreport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bugreport import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reportbug/', views.submit_ticket, name="reportbug"),
    path('', views.index, name="homepage"),
    path('changestatus/<int:id>', views.change_status, name="changestatus"),
    path("ticket/<int:id>", views.single_ticket, name="ticket view"),
    path("user/<int:id>", views.user_tickets, name="user"),
    path("edit/<int:id>", views.edit_ticket, name="edit")
]
