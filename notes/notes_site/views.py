from django.shortcuts import render
from django.http import HttpResponse
from notes_site.models import (Note)
from notes_site.service import (
    register_save,
    activation,
    authorization,
    restore_password,
    get_context_auth,
    get_context_reg,
    get_notes,
    edit_notes,
    delete_note
    )
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
        return HttpResponse(
            request,
            context=auth
            )


class RegisterView(View):
    def post(self,request):
        save = register_save(request)
        return HttpResponse(
            )

class RestorePassword(View):
    def post(self,request):
        restore =  restore_password(request)
        return HttpResponse(
            request,
            context = restore
        )

class ActivateView(View):
    def get(self,request,hash):
        answer = activation(hash)
        return HttpResponse(#????????HttpResp
            '234'
            )


class NoteCreateView(View):
    def post(self,request):
        create = edit_notes(request)
        return HttpResponse(
            request,
            context=create
            )


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'


class NoteDeleteView(View):
    def post(self,request):
        delete = delete_note(request)
        return HttpResponse(
            request,
            context=delete
            )
