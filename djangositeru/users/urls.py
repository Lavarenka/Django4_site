from django.urls import path
from . import views

"""
урлы приложения users
не забыть подключить в основных урлах
"""

app_name = "users"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

]
