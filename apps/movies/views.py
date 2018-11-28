from django.shortcuts import render
from django.urls import reverse_lazy
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
            context['my_rating'] = self.object.rating_set.filter(user=self.request.user).first
        return context


class RatingCreate(LoginRequiredMixin, CreateView):
    http_method_names = ['post',]
    model = Rating
    fields = ['score',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = self.kwargs.get('movie_id')
        return super().form_valid(form)
