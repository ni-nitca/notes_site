from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from notes_site.service import register_save
from django.template.loader import render_to_string
from django.core.mail import EmailMessage 
from django.contrib.sites.shortcuts import get_current_site
from notes_site.models import User
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text 



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
    template_name = ''
    if request.method == "POST":
        data = request.POST
        hash = register_save(data)
        current_site = get_current_site(request) 
        mail_subject = 'Ссылка активации отправлена на вашу электронную почту'
        message = render_to_string('acc_active_email.html', { 
                'user': user, 
                'domain': current_site.domain, 
                'url': urlsafe_base64_encode(force_bytes(hash))
            })
        to_email = data.get('email')
        email = EmailMessage(
            mail_subject,
            message,
            to=to_email
        )
        email.send
        return HttpResponse('Пожалуйста проверьте вашу почту для завершения регистрации')
    else:
        return render(request, template_name)
         

def activate(request):
    user = User()
    hash = user.hash
    uid = force_text(urlsafe_base64_decode(hash))
    if user is not None and hash == uid:
        user.is_active = True
        user.save()

