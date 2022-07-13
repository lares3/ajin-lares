
from rest_framework import serializers
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import DjangoUnicodeDecodeError

class Emailserializer(serializers.Serializer):
    email =serializers.EmailField()

    class Meta:
        fields=("email",)

class ResetPasswordSerializer(serializers.Serializer):
    password= serializers.CharField(
        write_only=True,
        min_length=6
        )
    password2= serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        fields= ["password","password2",]

    def validate(self, data):
        try:
            password= data.get("password")
            password2= data.get("password2")
            token= self.context.get("kwargs").get("token")
            encoded_pk= self.context.get("kwargs").get("encoded_pk")

            if password != password2:
                raise serializers.ValidationError("password1 and password2 doesn't match")
        
            if token is None or encoded_pk is None:
                serializers.ValidationError("Missing Data")
            
            pk = urlsafe_base64_decode(encoded_pk).decode()
            user= User.objects.get(pk=pk)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The Reset Token Is Invalid")

            user.set_password(password)
            user.save()
            return data
            
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("password1 and password2 doesn't match")