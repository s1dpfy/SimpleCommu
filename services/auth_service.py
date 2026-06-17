from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from accounts.models import User

class AuthService:
    @staticmethod
    def register(username, password):
        try:
            user = User.objects.create_user(username=username, password=password)
            return user
        except IntegrityError:
            raise ValidationError("이미 존재하는 사용자 이름입니다.")

    @staticmethod
    def login(request, username, password):
        user = authenticate(request, username=username, password=password)
        if not user:
            raise ValidationError("자격 증명이 유효하지 않습니다.")
        if user.banned:
            raise ValidationError("정지된 계정입니다.")
        login(request, user)
        return user

    @staticmethod
    def logout(request):
        logout(request)