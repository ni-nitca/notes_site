from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import login
from notes_site.models import (Note)
from django.contrib.auth.views import LogoutView
from notes_site.service import (
    register_save,
    activation,
    authorization,
    restore_password,
    get_context_auth,
    get_notes,
    edit_notes,
    delete_note,
    inventig_password,
    get_note
    )
from django.views.generic import (
    View,
    DetailView,
)


class IndexView(View):
    def get(self, request):
        template_name = 'notes_site/index.html'
        if request.user.is_authenticated:
            context = get_notes(request)
        else:
            context = get_context_auth()
        return render(request, template_name, context)
    def post(self, request):
        template_name = 'notes_site/index.html'
        answer = get_notes(request)
        return render(request, template_name, answer)


class AutorizeView(View):
    def get(self,request):
        template_name = 'notes_site/post_auth.html'
        return render(request,template_name)
    def post(self,request):
        template_name = 'notes_site/post_auth.html'
        auth = authorization(request)
        return render(request,template_name, auth)


class UserLogoutView(LogoutView):
    next_page = 'home'


class RegisterView(View):
    def get(self,request):
        template_name = 'notes_site/post_register.html'
        return render(request,template_name)
    def post(self,request):
        template_name = 'notes_site/post_register.html'
        save = register_save(request)
        return render(request, template_name, save)

class RestorePassword(View):
    def get(self,request):
        template_name = 'notes_site/post_restore_pass.html'
        return render(request, template_name) 
    def post(self,request):
        template_name = 'notes_site/post_restore_pass.html'
        restore =  restore_password(request)
        return render(request, template_name, restore)


class InventingPassword(View):
    def get(self,request,hash):
        template_name = 'notes_site/post_inventing.html'
        answer = activation(hash)
        return render(request,template_name,answer)
    def post(self,request):
        template_name = 'notes_site/post_inventing.html'
        answer = inventig_password(request)
        return render(request, template_name, answer)


class ActivateView(View):
    def get(self,request, hash):
        template_name = 'notes_site/activated.html'
        answer = activation(hash)
        return render(request, template_name, answer)


class NoteCreateView(View):
    def get(self,request):
        template_name = 'notes_site/add_note.html'
        return render(request,template_name)
    def post(self,request):
        template_name = 'notes_site/add_note_status.html'
        create = edit_notes(request)
        return render(request,template_name, create)


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'


class NoteEditView(View):
    def get(self,request,slug):
        template_name = 'notes_site/edit_note.html'
        answer = get_note(slug)
        return render(request, template_name, answer)    
    def post(self,request):
        template_name = 'notes_site/add_note_status.html'
        create = edit_notes(request)
        return render(request, template_name, create)


class NoteDeleteView(View):
    def get(self,request,slug):
        template_name = 'notes_site/delete_note.html'
        answer = get_note(slug)
        return render(request, template_name, answer)
    def post(self,request):
        template_name = 'notes_site/delete_note.html'
        delete = delete_note(request)
        return render(request, template_name, delete)
