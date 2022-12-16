from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import User
from rest_framework.authtoken.models import Token
from Watches.models import Watch


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'password2']

    def validate_email(self, email):
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError('Email already taken!')
        return email

    def validate_phone(self, phone):
        if len(phone) == 13 and phone[1:].isdigit() and phone[:4] == '+996':
            return phone
        raise ValidationError('Phone is incorrect format')

    def save(self, *args, **kwargs):

        user = User(
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password2 != password:
            raise ValidationError({password: "Passwords not match"})

        user.set_password(password)
        user.save()
        Watch.objects.create(user=user)
        return user