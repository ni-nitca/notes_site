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
    get_notes
)


class ServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": 'mr@mail.ru', "password1": '12345', "password2": '12345'}
        cls.data1 = {"email": 'mr@mail.ru', "password1": '12345', "password2": '12345'}
        cls.email = "mr@mail.ru"
        cls.is_superuser = False
        cls.is_staff = False
        cls.is_active = True
        cls.get_data = {"tags":"1,3,4,6"}
        cls.title = "123"
        cls.description = "321"
        cls.slug = "123"
        cls.data2 = []

    def test_register_save(self):
        data = self.data
        answer = {
          "status_code":200,
          "text":"Все прошло успешно"
        }
        self.assertEqual(answer, register_save(data))

        data = self.data1
        answer = {
            "status_code":402,
            "text":"Ваша почта уже используется"
        }
        self.assertEqual(answer, register_save(data))

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



