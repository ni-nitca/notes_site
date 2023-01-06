from django.urls import path 
from django.contrib.auth import views as auth_views
from notes_site.views import (
    IndexView,
    AutorizeView,
    RegisterView,
    ActivateView,
    NoteDetailView,
    NoteCreateView,
    NoteDeleteView
)


urlpatterns = [
    path('home/', IndexView.as_view(), name = 'home'),
    path('home/', AutorizeView.as_view(), name = 'authorize'),
    path('home/', RegisterView.as_view(), name = 'registrarion'),
    path('activate/<str:hash>', ActivateView.as_view(), name = 'activate'),
    path('note/<str:slugify>',NoteDetailView.as_view(),name = 'note-detail'),
    path('note/new', NoteCreateView.as_view(), name = 'note-create'),
    path('note/<str:slugify>/delete',NoteDeleteView.as_view(),name = 'delete-view'),
]