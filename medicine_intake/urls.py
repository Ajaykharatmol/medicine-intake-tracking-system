from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
   
    path('CreateUserRegister/', views.CreateUserRegister.as_view()),

    path('LoginUser/', views.AppToken.as_view()),

    path('GetUserProfileDetails/', views.GetUserProfileDetails.as_view()),

    path('GetUserProfileDetails/<pk>', views.GetUserProfileDetails.as_view()),
    
    path('reset_password/',
         auth_views.PasswordResetView.as_view(),
         name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(),
     name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="dashboard/password_reset_done.html"),
        name="password_reset_complete"),

    path('Medicine/', views.MedicineList.as_view()),
    path('Medicine/<int:pk>/', views.MedicineDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)