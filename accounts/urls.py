from django.urls import path

from accounts import views


app_name = 'accounts'


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('activate/<str:username>/<str:token>/', views.activate_account_view, name='activate'),
    path('login/', views.login_view, name='login')
]
