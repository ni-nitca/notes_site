from notes_site.models import (
    Note,
    EmailHash,
    User,
    Authorize,
    Registration,
    MailSettings,
)
from django.http import HttpResponse
from django.contrib.auth import authenticate
from notes_site.check import (
    check_reg_password,
    check_register_data,
    check_authorize_data,
)

from django.template.loader import render_to_string
from django.core.mail import EmailMessage 
from django.contrib.auth.hashers import make_password



def authorization(data):
    if not check_authorize_data(data):
        answer = {
            "status_code":400,
            "text": "Неверные данные"
            }
        return answer

    username = data['email']
    password = data['password']
    user = authenticate(username,password)
    if user.is_active:
        return user
    else:
        answer = {
        "status_code":400,
        "text": "Аккаунт не активирован"
        }
        return answer 


def register_save(data):
    user = User()
    if not check_register_data(data):
        answer = {
            "status_code":400,
            "text": "Неверно передан словарь"
        }
        return answer
    if not check_reg_password(data):
        answer = {
            "status_code":400,
            "text":"Пароли не равны между собой"
        }
        return answer

    user.email = data.get('email')
    user.password = make_password(data.get('password1'))
    user.save()
    hash_obj = EmailHash.objects.create(user=user)
    hash = hash_obj.hash_text

    email_send(data,hash)
    answer = {
        "status_code":200,
        "text":"Все прошло успешно"
    }
    return answer


def email_send(data,hash):
    mail_obj = MailSettings.objects.get_or_create(pk=1)
    mail_set = mail_obj[0]
    current_site = mail_set.domen
    mail_subject = mail_set.description

    template_name = "notes_site/acc_active_email.html"
    message = render_to_string(template_name, {
        'domain': current_site, 
        'token': hash,
    })
    to_email = data.get('email')
    email = EmailMessage(
        mail_subject,
        message,
        to=[to_email]
    )
    email.send()
    return 'Пожалуйста проверьте вашу почту для завершения регистрации'


def activation(hash):
    user_hash = EmailHash.objects.get(hash_text= hash) 
    user_id = user_hash.user_id
    user = User.objects.get(pk=user_id)
    if user is not None and hash is not None:
        user.is_active = True
        user.save()
        answer = {
            "status_code":200,
            "text":"Вы успешно активировали ваш аккаунт"
        }
        return answer
    else:
        answer = {
            "status_code":404,
            "text":"Некорректаная ссылка"
        }
        return answer
        

def get_notes(request):
    user = request.user
    user_id = User.objects.filter(email=user)
    notes = Note.objects.filter(user_id = user)
    data = {"notes":notes}
    return data

def search_notes(request):
    data = request.POST
    user = request.user
    tags = data.get('tags')
    notes = get_notes(request)


def edit_notes(data,request):
    user = request.user
    note = Note()
    note.user = user
    note.title = data.get('title')
    note.description = data.get('descriptions')
    



    