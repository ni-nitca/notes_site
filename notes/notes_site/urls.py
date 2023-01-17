from django.urls import path
from django.contrib.auth import views as auth_views
from notes_site.views import (
    IndexView,
    AutorizeView,
    RegisterView,
    RestorePassword,
    InventingPassword,
    ActivateView,
    NoteDetailView,
    NoteCreateView,
    NoteDeleteView,
    LogoutView,
    NoteEditView,
)


urlpatterns = [
    path('', IndexView.as_view(), name = 'home'),
    path('auth/', AutorizeView.as_view(), name = 'authorize'),
    path('register/', RegisterView.as_view(), name = 'registrarion'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('restore/', RestorePassword.as_view(), name = 'restore'),
    path('inventing/', InventingPassword.as_view(), name = 'invent'),
    path('activate/<str:hash>', ActivateView.as_view(), name = 'activate'),
    path('note/<slug:slug>',NoteDetailView.as_view(),name = 'note-detail'),
    path('note/new', NoteCreateView.as_view(), name = 'note-create'),
    path('note/edit/<str:slug>', NoteEditView.as_view(), name="npte-edit"),
    path('note/<str:slugify>/delete',NoteDeleteView.as_view(),name = 'delete'),
]
