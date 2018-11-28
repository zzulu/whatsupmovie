from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Movie, Rating
from .forms import RatingForm


class MovieList(ListView):
    model = Movie
    context_object_name = 'movies'


class MovieDetail(DetailView):
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = RatingForm()
        if self.request.user.is_authenticated:
            context['rating_exists'] = self.object.rating_set.filter(user=self.request.user).exists()
        return context


class RatingCreate(LoginRequiredMixin, CreateView):
    http_method_names = ['post',]
    model = Rating
    form_class = RatingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = self.kwargs.get('movie_id')
        return super().form_valid(form)


class RatingDelete(LoginRequiredMixin, DeleteView):
    http_method_names = ['post',]
    model = Rating

    def get_success_url(self):
        return reverse('movies:detail', kwargs={'pk':self.kwargs.get('movie_id')})

    def delete(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this Comment")
        return super().delete(request, *args, **kwargs)
