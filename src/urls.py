
from django.contrib import admin
from django.urls import path
from first import views

urlpatterns = [

    path ("password.reset/",
    views.PasswordReset.as_view() ,
    name="reset_password"),

    path ("password.reset/<str:encoded_pk>/<str:token>/",
    views.ResetPassword.as_view(),
    name="reset_password"),

    path('admin/', admin.site.urls),
]
