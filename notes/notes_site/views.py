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
    get_context_reg,
    get_notes,
    edit_notes,
    delete_note,
    inventig_password
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


class AutorizeView(View):
    def get(self,request):
        template_name = ''
        return render(request,template_name)
    def post(self,request):
        template_name = ''
        auth = authorization(request)
        return reverse_lazy(request,template_name, auth)


class UserLogoutView(LogoutView):
    next_page = 'home'


class RegisterView(View):
    def get(self,request):
        template_name = ''
        return render(request,template_name)
    def post(self,request):
        template_name = ''
        save = register_save(request)
        return render(request, template_name, save)

class RestorePassword(View):
    def get(self,request):
        template_name = ''
        return render(request, template_name) 
    def post(self,request):
        template_name = ''
        restore =  restore_password(request)
        return render(request, template_name, restore)


class InventingPassword(View):
    def get(self,request,hash):
        template_name = ''
        answer = activation(hash)
        return render(request,template_name,answer)
    def post(self,request):
        template_name = ''
        answer = inventig_password(request)
        return render(request, template_name, answer)


class ActivateView(View):
    def get(self,request, hash):
        template_name = ''
        answer = activation(hash)
        return render(request, template_name, answer)


class NoteCreateView(View):
    def get(self,request):
        template_name = ''#если есть slug вернуть словарь
        return render(request,template_name)
    def post(self,request):
        create = edit_notes(request)
        return JsonResponse(create)


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'
    #что содержит detail переставить с id в slug
class NoteEditView(View):
    def get(self,request):
        template_name = ''
        return render(request,template_name)    
    def post(self,request):
        create = edit_notes(request)
        return JsonResponse(create)

class NoteDeleteView(View):
    def get(self,request):
        template_name = ''
        return render(request,template_name)
    def post(self,request):
        delete = delete_note(request)
        return JsonResponse(delete)
