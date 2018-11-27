from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


class Login(LoginView):
    redirect_authenticated_user = True


class Logout(LogoutView):
    pass


class Signup(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('movies:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response