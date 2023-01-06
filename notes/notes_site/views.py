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
        template_name = ''
        auth = authorization(request)
        return render(
            request,
            template_name,
            context=auth
            )


class RegisterView(View):
    def post(self,request):
        template_name = ''
        save = register_save(request)
        return render(
            request,
            template_name,
            context=save
            )
         

class ActivateView(View):
    def get(request):
        template_name = ''
        hash = request.get('hash')
        answer = activation(hash)
        return render(
            request,
            template_name,
            context=answer
            )


class NoteCreateView(View):
    def post(request):
        template_name = ''
        create = edit_notes(request)
        return render(
            request,
            template_name,
            context=create
            )


class NoteDetailView(DetailView):
    model = Note


class NoteDeleteView(View):
    def post(request):
        template_name = ''
        delete = delete_note(request)
        return render(
            request,
            template_name,
            context=delete
            )






