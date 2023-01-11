from django.shortcuts import render
from django.http import JsonResponse
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
    delete_note,
    inventig_password
    )
from django.views.generic import (
    View,
    DetailView
)


class IndexView(View):
    def get(self, request):
        template_name = 'index.html'
        if request.user.is_authenticated:
            context = get_notes(request)
        else:
            context = get_context_auth()
        return render(request, template_name, context)


class AutorizeView(View):
    def post(self,request):
        auth = authorization(request)
        return JsonResponse(
            auth
            )

##logout

class RegisterView(View):
    def post(self,request):
        save = register_save(request)
        return JsonResponse(
            save
            )

class RestorePassword(View):
    def post(self,request):
        restore =  restore_password(request)
        return JsonResponse(restore)


class InventingPassword(View):
    def get(self,hash):
        answer = activation(hash)
        return JsonResponse(answer)
    def post(self,request,hash):
        answer = inventig_password(request,hash)
        return JsonResponse(answer)


class ActivateView(View):
    def get(self, hash):
        answer = activation(hash)
        return JsonResponse(answer)


class NoteCreateView(View):
    def post(self,request):
        create = edit_notes(request)
        return JsonResponse(create)


class NoteDetailView(DetailView):
    model = Note
    context_object_name = 'note'


class NoteDeleteView(View):
    def post(self,request):
        delete = delete_note(request)
        return JsonResponse(delete)
