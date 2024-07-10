from django.urls import path
from .views import *

app_name = 'shortener'

urlpatterns = [
    path('create/', LinkCreateView.as_view(), name='create_link'),
    path('delete/<pk>', LinkDeleteView.as_view(), name='delete_link'),
    path('<code>/', LinkRedirect.as_view()),
    path('detail/<pk>/<code>/', LinkDetailView.as_view(), name='detail'),
    path('links/list', LinkListView.as_view(), name='links')
]
