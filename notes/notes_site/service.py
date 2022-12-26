from notes_site.models import (
    Note,
    EmailHash,
    User,
    Authorize,
    Registration,
)
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from notes_site.check import (
    check_reg_password,
    check_register_data,

)

from django.template.loader import render_to_string
from django.core.mail import EmailMessage 
from django.contrib.sites.shortcuts import get_current_site



def register_save(data,request):
    user = User()
    if not check_register_data(data):
        answer = {
            "code":400,
            "text": "Неверно передан словарь"
        }
        return answer
    if not check_reg_password(data):
        answer = {
            "code":200,
            "text":"Пароль не равны между собой"
        }
        return answer
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')
    user.password = data.get('password1')

    EmailHash.objects.create(user=user)
    user.save()
    hash = EmailHash.objects.filter(user=user)
    email_send(data,request,user,hash)
    answer = {
        "answer":200,
        "text":"Все прошло успешно"
    }
    return answer


def email_send(data,request,user,hash):
    current_site = get_current_site(request) 
    mail_subject = 'Ссылка активации отправлена на вашу электронную почту'
    message = render_to_string('acc_active_email.html', { 
                'user': user, 
                'domain': current_site.domain, 
                'url': hash
            })
    to_email = data.get('email')
    email = EmailMessage(
            mail_subject,
            message,
            to=to_email
        )
    email.send
    return 'Пожалуйста проверьте вашу почту для завершения регистрации'

def activation(request):
    user = User()
    hash = EmailHash.objects.filter(user=user)
    if user is not None and hash is not None:
        user.is_active = True
        user.save()
        answer = {
            "code":200,
            "text":"Вы успешно активировали ваш аккаунт"
        }
        return answer
    else:
        answer = {
            "code":404,
            "text":"Некорректаная ссылка"
        }
        return answer
        

def get_notes(request):
    user = request.user
    notes = Note.objects.filter(user_id = user)
    data = {"notes":notes}
    return data