from notes_site.models import (
    Note,
    Hash,
    Authorize,
    Registration,
    User
)
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def check_register_json(file_of_json):
    if file_of_json != []:
        values = file_of_json.keys()
        true_list = [
            "username",
            "email",
            "password1",
            "password2",
        ]
        for value in true_list:
            if value not in values:
                return False
        return True
    else:
        return False

def register_save(req):
    user = User()
    if req.method == "POST":
        data = req.POST
        if check_register_json(data):
            user.username = data['username']
            user.email = data['email']
            user.password = data['password1']  #check пароля будет производится на фронте?



def autorize(req):
    if req.method == 'POST':
        data = req.POST
        user = authenticate(username=data['username'],password=data['password'])
        if user is not None:
            if user.is_active:
                return login(req,user)
            else:
                return HttpResponse('Аккаунт не активирован')
        else:
            return HttpResponse('Неверный логин или пароль')
    else:
        return render (req,template_name)

