from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Link
from hashids import Hashids
from .forms import LinkForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

@method_decorator(login_required, name='dispatch')
class LinkCreateView(CreateView):
    form_class = LinkForm
    template_name = 'shortener/create_link.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('shortener:detail', args=[self.object.id, self.object.code])

class LinkRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        try:
            link_id = Hashids(min_length=8).decode(self.kwargs['code'])[0]
            link = Link.objects.filter(id=link_id).first()
            if link:
                link.clicks += 1
                link.last_click = timezone.now()
                link.save()
                return link.url
            else:
                raise Http404("Este enlace no existe")
        except IndexError:
            raise Http404("Este enlace no existe")

@method_decorator(login_required, name='dispatch')       
class LinkDetailView(DetailView):
    model = Link

    def get_object(self):
        obj = get_object_or_404(Link, created_by=self.request.user, pk=self.kwargs['pk'])
        return obj

@method_decorator(login_required, name='dispatch')
class LinkListView(ListView):
    model = Link
    paginate_by = 10

    def get_queryset(self):
        queryset = super(LinkListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)
    
@method_decorator(login_required, name='dispatch')  
class LinkDeleteView(DeleteView):
    model = Link
    success_url = reverse_lazy('shortener:links')

    def get_object(self):
        obj = get_object_or_404(Link, created_by=self.request.user, pk=self.kwargs['pk'])
        return obj