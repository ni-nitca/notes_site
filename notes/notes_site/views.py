from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login
from notes_site.models import (Note)
from notes_site.service import (
    register_save,
    activation,
    authorization,
    get_context_auth,
    get_context_reg,
    get_notes,
    edit_notes,
    delete_note
    )
from django.core.mail import EmailMessage 
from notes_site.models import User
from django.views.generic import (
    View,
    DetailView
)



class IndexView(View):
    def get(self, request):
        template_name = ''
        if request.user.is_authenticated:
            context = get_notes(request)
        else:
            context = get_context_auth()
        return render(request, template_name, context)


class AutorizeView(View):
    def post(self,request):
        auth = authorization(request)
        return render(
            request,
            context=auth
            )


class RegisterView(View):
    def post(self,request):
        save = register_save(request)
        return render(
            request,
            context=save
            )
         

class ActivateView(View):
    def get(self,request,hash):
        answer = activation(hash)
        return render(
            request,
            context=answer
            )


class NoteCreateView(View):
    def post(self,request):
        create = edit_notes(request)
        return render(
            request,
            context=create
            )


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'


class NoteDeleteView(View):
    def post(request):
        delete = delete_note(request)
        return render(
            request,
            context=delete
            )






