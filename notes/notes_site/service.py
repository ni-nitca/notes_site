from notes_site.models import (
    Note,
    EmailHash,
    User,
    Authorize,
    Registration,
    MailSettings,
    Tags,
)
from notes_site.check import (
    check_reg_password,
    check_register_data,
    check_authorize_data,
    check_notes,
    check_tags
)
from slugify import slugify
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4

def authorization(request):
    data = request.data
    if not check_authorize_data(data):
        answer = {
            "status_code":400,
            "text": "Неверные данные"
            }
        return answer

    email = data.get('email')
    password = data.get('password')
    user = User.objects.filter(email=email)[0]
    us_password = user.password

    data_pas = {
        'email':email,
        'password1':password,
        'password2':us_password
        }

    if not user.exists():
        answer = {
            "status_code":401,
            "text":"Неверный логин или пароль"
        }
        return answer
    if not check_reg_password(data_pas):
        answer = {
            "status_code":402,
            "text":"Неверный логин или пароль"
        }
        return answer

    if not user.is_active:
        answer = {
            "status_code":403,
            "text": "Аккаунт не активирован"
        }
        return answer

    answer = {
        "status_code":200,
        "text":"Успешная авторизация"
        }
    return answer


def register_save(request):
    data = request.data
    if not check_register_data(data):
        answer = {
            "status_code":400,
            "text": "Неверно передан словарь"
        }
        return answer

    if not check_reg_password(data):
        answer = {
            "status_code":401,
            "text":"Пароли не равны между собой"
        }
        return answer

    user = User()
    email = data.get('email')
    password = data.get('password1')
    email_in_db = User.objects.filter(email=email)

    if email_in_db:
        answer = {
            "status_code":402,
            "text":"Ваша почта уже используется"
        }
        return answer
    
    user.email = email
    user.password = make_password(password)
    user.save()
    hash_obj = EmailHash.objects.create(user=user)
    hash = hash_obj.hash_text

    email_send(email, hash)
    answer = {
        "status_code":200,
        "text":"Все прошло успешно"
    }
    return answer


def email_send(email, hash, repeat = False):
    to_email = email
    mail_obj = MailSettings.objects.get_or_create(pk=1)[0]
    current_site = mail_obj.domen
    mail_subject = mail_obj.title

    template_name = "notes_site/acc_active_email.html"
    message = render_to_string(template_name, {
        'domain': current_site,
        'token': hash,
    })

    send_mail(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    if not repeat:
        return 'Пожалуйста проверьте вашу почту для завершения регистрации'
    else:
        return 'Для завершения смены пароля перейдите по ссылке на почте'


def activation(hash):
    user_hash = EmailHash.objects.filter(hash_text=hash)[0]
    if user_hash:
        user = user_hash.user
        if user is not None:
            user.is_active = True
            user.save()
            answer = {
                "status_code":200,
                "text":"Вы успешно активировали ваш аккаунт"
            }
            return answer
    answer = {
        "status_code":404,
        "text":"Некорректаная ссылка"
    }
    return answer

def restore_password(request):
    data = request.data
    if not check_register_data(data):
        answer = {
            "status_code":400,
            "text": "Неверные данные"
            }
        return answer
    if not check_reg_password(data):
        answer = {
            "status_code":401,
            "text":"Пароли не равны между собой"
        }
        return answer

    email = data.get("email")
    password = data.get('password1')

    user = User.objects.filter(email=email)[0]
    if not user.exists():
        answer = {
            "status_code":401,
            "text":"Аккаунт не найден"
        }
        return answer
    user.is_active = False
    password = make_password(password)
    user.update(password)
    hash_obj = EmailHash.objects.filter(user=user)[0]
    hash = uuid4
    hash_obj.update(hash)

    email_send(email, hash)
    answer = {
        "status_code":200,
        "text":"Все прошло успешно"
    }
    return answer


def get_notes(request):
    user = request.user
    data = request.data
    notes = Note.objects.filter(user_id=user)

    if not check_tags(data):
        answer = {"notes":notes}
        return answer

    tags = data.get("tags")
    tags_list = tags.split(',')
    notes = notes.filter(tags__in = tags_list)
    answer = {"notes":notes}

    return answer


def edit_notes(request):
    data = request.data
    if not check_notes(data):
        answer = {
            "status_code":400,
            "text":"передан пустой или некорректный словарь"
        }
        return answer

    user = request.user
    pk = data.get('id')
    title = data.get('title')
    description = data.get('description')
    slug = slugify(title)
    tags = data.get('tag')
    tags_list = tags.split(',')

    if pk is None:
        note = Note.objects.create(
            user,title,description,slug
            )
    else:
        note = Note.objects.filter(id=pk)[0]
        note.delete()
        note = Note.objects.create(
            user,title,description,slug
            )

    if tags_list:
        tags = [Tags(note = note,tags = tag) for tag in tags_list]
        Tags.objects.bulk_create(tags)

    answer ={
        "status_code":200,
        "text": "Все прошло успешно"
    }
    return answer


def delete_note(request):
    data = request.data

    if not check_notes(data):
        answer = {
            "status_code":400,
            "text":"передан пустой или некорректный словарь"
        }
        return answer

    pk = data.get('id')
    note = Note.objects.filter(id=pk)[0]

    if not note.exists():
        answer = {
            "status_code":401,
            "text":"Заметки не существует"
        }
        return answer

    note.delete()
    answer ={
        "status_code":200,
        "text": "Все прошло успешно"
    }
    return answer


def get_context_auth():
    authorize = Authorize.objects.get_or_create()[0]
    description = authorize.description
    answer = {
        "status_code":200,
        "text": description
    }
    return answer


def get_context_reg():
    registration = Registration.objects.get_or_create()[0]
    description = registration.description
    answer = {
        "status_code":200,
        "text": description
    }
    return answer
