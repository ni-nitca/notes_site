from django.test import TestCase

from notes_site.models import (
    User,
    Note,
    Tags,
    EmailHash,
    MailSettings
)

from notes_site.service import (
    register_save,
    email_send,
    get_notes,
    authorization,
    restore_password,
    inventig_password,
    edit_notes,
    delete_note
)
from uuid import uuid4



class ServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": 'mr@mail.ru', "password1": '12345', "password2": '12345'}
        cls.data1 = {"email": 'mr.chuvak.132@mail.ru', "password1": '12345', "password2": '12345'}
        cls.email = 'mr.chuvak.132@mail.ru'
        cls.pasword = '12345'
        cls.data_auth = {"email": 'mr.chuvak.132@mail.ru', "password":"12345"}
        cls.is_superuser = False
        cls.is_staff = False
        cls.is_active = True
        cls.get_data = {"tags":"1,3,4,6"}
        cls.title = "123"
        cls.description = "321"
        cls.slug = "123"
        cls.data2 = []



    def test_auth(self):
        user = User.objects.create(
            email = "mr.chuvak.132@mail.ru",
            is_active = False
        )
        data = {}
        auth_answ = authorization(data)
        answer = {
            "status_code":400,
            "text": "Неверные данные"
        }
        self.assertEqual(answer, auth_answ,msg=1)

        data = {"email": 'mr.chuvak.132@mail.r', "password":"12345"}
        auth_answ = authorization(data)
        answer = {
            "status_code":401,
            "text":"Неверный логин или пароль"
        }
        self.assertEqual(answer, auth_answ,msg=2)

        data = self.data_auth
        auth_answ = authorization(data)
        answer = {
            "status_code":402,
            "text":"Неверный логин или пароль"
        }
        self.assertEqual(answer, auth_answ,msg=3)
        user = User.objects.filter(email=self.email).first()
        user.set_password("12345")
        user.save()
        data =  self.data_auth
        auth_answ = authorization(data)
        answer = {
            "status_code":403,
            "text": "Аккаунт не активирован"
        }
        self.assertEqual(answer, auth_answ,msg=4)

        user.is_active = True
        user.save()
        user = User.objects.filter(email=self.email).first()
        data =  self.data_auth
        auth_answ = authorization(data)
        answer = {
            "status_code":200,
            "text":"Вы успешно авторизованы"
            }
        self.assertEqual(user, auth_answ,msg=5)

    def test_register_save(self):
        data = self.data
        answer = {
          "status_code":200,
          "text":"Все прошло успешно"
        }
        self.assertEqual(answer, register_save(data))

        data = self.data
        answer = {
            "status_code":402,
            "text":"Ваша почта уже используется"
        }
        self.assertEqual(answer, register_save(data))


    def test_email(self):
        user = User.objects.create(
        email = self.email,
        password = '12345',
        is_active = True
        )
        hash_obj = EmailHash.objects.create(user=user)
        hash = hash_obj.hash_text
        answer = 'Пожалуйста проверьте вашу почту для завершения регистрации'
        data = {'email':self.email}
        auth = email_send(data,hash)
        self.assertEqual(answer, auth)

    
    def test_restore_password(self):
        data = self.data_auth
        answer = {
            "status_code":400,
            "text":"Неверные данные"
        }
        self.assertEqual(answer, restore_password(data))

        data = self.data
        answer = {
            "status_code":401,
            "text":"Аккаунт не найден"
        }
        self.assertEqual(answer, restore_password(data))

        data = self.data
        user = User.objects.create(
        email = "mra@mail.ru",
        password = '12345',
        is_active = False
        )
        answer = {
            "status_code":402,
            "text":"Для восстановления пароля,завершите регистрацию"
        }
        self.assertEqual(answer, restore_password(data))

        data = self.data
        user = User.objects.filter(email = self.data.get("email"))
        active = True
        user.update(is_active = active)
        answer = {
            "status_code":403,
            "text":"Хэша не найдено"
        }
        self.assertEqual(answer, restore_password(data))
        data = self.data1
        user = User.objects.create(
        email = "mr.chuvak.132@mail.ru",
        password = '12345',
        is_active = True
        )
        user = User.objects.filter(email = self.data1.get("email"))
        user = user.first()
        hash_obj = EmailHash.objects.create(user=user)
        answer = {
        "status_code":200,
        "text":"Все прошло успешно"
        }
        self.assertEqual(answer, restore_password(data),msg="cool")

    def test_inventing_password(self):
        data = self.data_auth
        answer = {
            "status_code":401,
            "text":"Неверно передан словарь"
        }
        self.assertEqual(answer, inventig_password(data), msg=1)

        user = User.objects.create(
        email = "mr.chuvak.132@mail.ru",
        password = '12345',
        is_active = True
        )
        hash = uuid4
        data = {"hash":f"{hash}","password1":"12345", "password2":"12345"}
        answer = {
            "status_code":402,
            "text":"Аккаунт по hash не найден"
        }
        self.assertEqual(answer, inventig_password(data),msg=2)

        user = User.objects.filter(email = self.data1.get("email"))
        user = user.first()
        hash_obj = EmailHash.objects.create(user=user)
        hash_obj = EmailHash.objects.filter(user=user)
        hash_obj = hash_obj.first()
        hash = hash_obj.hash_text
        data = {"hash":f"{hash}","password1":"12345", "password2":"12345"}
        answer = {
        "status_code":200,
        "text":"Все прошло успешно"
        }
        self.assertEqual(answer, inventig_password(data),msg=3)
    
    def test_get_notes(self):
        user = User.objects.create(
            email = self.email,
            password = 12345,
            is_active = True
        )
        note = Note.objects.create (
            user = user,
            title = self.title,
            description = self.description,
            slug = self.slug
        )
        answer = {"notes":[note]}
        answ_1 = get_notes(user,data=[]) 
        answ_1["notes"] = list(answ_1["notes"])
        self.assertEqual(answer, answ_1,msg=answ_1)

        tags = self.get_data.get("tags")
        tags_list = tags.split(',')
        obj = [
        Tags(
            note = note,
            tag = tag, 
        )
        for tag in tags_list
        ]
        Tags.objects.bulk_create(obj)
        notes = Note.objects.filter(user_id = user)
        note = notes.filter(tags__in = tags_list)
        answer = {"notes":note}
        self.assertEqual(answer, get_notes(user,self.get_data))
    
    def test_edit_notes(self):
        user = User.objects.create(
        email = "ikontai4@gmail.com",
        password = '12345',
        is_active = True
        )
        data = {}
        e_notes = edit_note(data,user)
        answer = {
            "status_code":400,
            "text":"передан пустой или некорректный словарь"
        }
        self.assertEqual(answer, e_notes, msg=1)

        User.objects.create(
        email = "mr.chuvak.132@mail.ru",
        password = '12345',
        is_active = True
        )
        slug = ''
        title = 'привет'
        description = '12'
        user = User.objects.filter(email="mr.chuvak.132@mail.ru" )
        user = user.first()
        data = {"slug":slug,"title":title,"description":description,"tags":'' }
        e_notes = edit_notes(data,user)
        answer ={
            "status_code":200,
            "text": "Все прошло успешно"
        }
        self.assertEqual(answer, e_notes,msg=2)

        note = Note.objects.filter(title=title).first()
        slug = note.slug
        title = 'привет т'
        description = '15'
        data = {"slug":slug,"title":title,"description":description,"tags":'' }
        ed_notes = edit_notes(data,user)
        answer ={
            "status_code":200,
            "text": "Все прошло успешно"
        }
        self.assertEqual(answer, ed_notes,msg=3)


        note = Note.objects.filter(title=title).first()
        note.delete()
        slug = ''
        title = 'привет'
        description = '12'
        user = User.objects.filter(email="mr.chuvak.132@mail.ru" )
        user = user.first()
        data = {"slug":slug,"title":title,"description":description,"tags":'1 2 3 4' }
        e_notes = edit_notes(data,user)
        answer ={
            "status_code":200,
            "text": "Все прошло успешно"
        }
        self.assertEqual(answer, e_notes,msg=4)
        
        note = Note.objects.filter(title=title).first()
        slug = note.slug
        title = 'привет t'
        description = '15'
        user = User.objects.filter(email="mr.chuvak.132@mail.ru" )
        user = user.first()
        data = {"slug":slug,"title":title,"description":description,"tags":'6 7 8 9' }
        e_notes = edit_notes(data,user)
        answer ={
            "status_code":200,
            "text": "Все прошло успешно"
        }
        self.assertEqual(answer, e_notes,msg=5)

    def test_delete_notes(self):
        user = User.objects.create(
            email = "mr.chuvak.132@mail.ru",
            password = '12345',
            is_active = True
        )
        data = {}
        d_notes = delete_note(data,user)
        answer = {
            "status_code":400,
            "text":"передан пустой или некорректный словарь"
        }
        self.assertEqual(answer, d_notes,msg=1)

        slug = ''
        title = 'привет'
        description = '12'
        user = User.objects.filter(email="mr.chuvak.132@mail.ru")
        user = user.first()
        data = {"slug":slug,"title":title,"description":description,"tags":'' }
        e_notes = edit_notes(data,user)
        data = {"slug":'1',"title":title,"description":description,"tags":'' }
        answer = {
            "status_code":401,
            "text":"Заметки не существует"
        }
        d_notes = delete_note(data,user)
        self.assertEqual(answer, d_notes,msg=2)

        note = Note.objects.filter(title=title).first()
        slug = note.slug
        data = {"slug":slug,"title":title,"description":description,"tags":'' }
        answer ={
            "status_code":200,
            "text": "Все прошло успешно"
        }
        d_notes = delete_note(data,user)
        note = Note.objects.filter(title=title).first()
        print(note)
        self.assertEqual(answer, d_notes,msg=3)

        


        







