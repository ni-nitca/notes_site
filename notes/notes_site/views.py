from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from notes_site.service import (
    register_save,
    activation,
    authorization,
    )
from django.core.mail import EmailMessage 
from notes_site.models import User
from django.views.generic import (
    ListView,
)



class Autorize(ListView):
    def get(self,request):#context?
        template_name = ""
        return render(request,template_name)

    def post(self,request):
        data = request.POST
        auth = authorization(data)
        if auth.get('status_code')==400:
            return HttpResponse(auth.get('text'))
        else:
            login(request,auth)


class Register(ListView):
    def get(self,request):
        template_name = 'notes_site/signup.html'
        return render(request, template_name)

    def post(self,request):
        template_name = ''
        data = request.POST
        save = register_save(data)
        status_code = save.get('status_code')
        text = save.get('text')
        if status_code == 400:
            return render(request,template_name,text)
        else:
            return render(request,template_name,text)        
         

class Activate(ListView):
    def get(self,request):
        template_name = ''
        hash = request.GET.get('hash')
        answer = activation(hash)
        status_code = answer.get("status_code")
        text = answer.get("text")
        if status_code == 400:
            return HttpResponse(text)
        else:
            return render(request,template_name)



