from django.test import TestCase

from notes_site.models import (
    Note,
    EmailHash,
    MailSettings
)

from notes_site.service import (
    register_save,
    email_send
)


class ServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": 'mr@mail.ru', "password1": '12345', "password2": '12345'}
        cls.data1 = {"email": 'mr@mail.ru', "password1": '12345', "password2": '12345'}
    def test_register_save(self):
        data = self.data
        data1 = self.data1
        answer = {
        "status_code":200,
        "text":"Все прошло успешно"
        }
        answer1 = {
            "status_code":402,
            "text":"Ваша почта уже используется"
        }
        self.assertEqual(answer, register_save(data))
        self.assertEqual(answer1, register_save(data1))


