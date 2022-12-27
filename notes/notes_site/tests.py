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

    def test_register_save(self):
        data = self.data
        answer = answer = {
        "answer":200,
        "text":"Все прошло успешно"
        }
        self.assertEqual(answer, register_save(data))

    def     

