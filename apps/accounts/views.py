from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .models import Profile
from .forms import ProfileForm


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
        Profile.objects.create(user=user)
        login(self.request, user)
        return response


class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:profile_detail')


class ProfileDetail(LoginRequiredMixin, DetailView):
    def get_object(self):
        return self.request.user.profile


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm

    def get_object(self):
        return self.request.user.profile

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this Profile.")
        return super().dispatch(request, *args, **kwargs)
