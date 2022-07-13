
from rest_framework import generics, status, viewsets, response

from . import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class PasswordReset(generics.GenericAPIView):
    serializer_class= serializers.Emailserializer

    def post(self, request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data["email"]
        user= User.objects.filter(email=email).first()
        if user:
            encoded_pk= urlsafe_base64_encode (force_bytes(user.pk))
            token=PasswordResetTokenGenerator().make_token(user)

            reset_url= reverse(
                "reset_password",
                kwargs={"encoded_pk": encoded_pk, "token": token}
            )
            reset_url= f"localhost:8000{reset_url} "

            return response.Response(
                {
                    "messege": f"Your Password Reset Link: {reset_url} "
                }, status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"User Doesn't Exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

class ResetPassword(generics.GenericAPIView):
    serializer_class= serializers.ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):

        serializer= self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        if serializer.is_valid(raise_exception= True):
            return response.Response(
            { "message": "Password Reset Complete" },
            status=status.HTTP_200_OK,
        )


        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )