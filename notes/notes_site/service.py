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
import uuid



def register_save(data):
    user = User()
    hash = EmailHash()
    if not check_register_data(data) and not check_reg_password(data):
        return False
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')
    user.password = data.get('password1')
    hash_text = uuid(4)
    hash.hash_text = hash_text

    user.save()
    hash.save()
    return hash_text




    
        
        


