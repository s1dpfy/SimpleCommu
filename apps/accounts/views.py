from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.exceptions import ValidationError
from services.auth_service import AuthService

class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('workspace_list')
        return render(request, 'accounts/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            AuthService.register(username, password)
            return redirect('login')
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request, 'accounts/signup.html')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('workspace_list')
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            AuthService.login(request, username, password)
            return redirect('workspace_list')
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request, 'accounts/login.html')

class LogoutView(View):
    def post(self, request):
        AuthService.logout(request)
        return redirect('login')