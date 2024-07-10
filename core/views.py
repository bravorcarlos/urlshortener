from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('shortener:links'))
        else:
            return super().get(request, *args, **kwargs)