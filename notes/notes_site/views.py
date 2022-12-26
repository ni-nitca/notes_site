from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from notes_site.service import register_save,activation
from django.core.mail import EmailMessage 
from notes_site.models import User





def autorize(request):
    template_name = ""
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(username,password)
        if user is not None:
            if user.is_active:
                return login(request,user)
            else:
                return HttpResponse('Аккаунт не активирован')
        else:
            return HttpResponse('Неверный логин или пароль')
    else:
        return render (request,template_name)

def register(request):
    user = User()
    template_name = 'notes_site/signup.html'
    if request.method == "POST":
        data = request.POST
        register_save(data,request)
    else:
        return render(request, template_name)
         

def activations(request):
    template_name = "notes_site/acc_activate_email.html" 
    activation(request)
    return render(request,template_name)



