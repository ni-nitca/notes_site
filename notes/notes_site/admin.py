from django.contrib import admin
from solo.admin import SingletonModelAdmin
from notes_site.models import Note, Authorize, Registration


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    class Meta:
        model = Note
        fields = ["title", "description ", "posted_date","tags"]


@admin.register(Authorize)
class AuthorizeAdmin(SingletonModelAdmin):
    class Meta:
        model = Authorize
        fields = ['description']


@admin.register(Registration)
class RegisterAdmin(SingletonModelAdmin):
    class Meta:
        model = Registration
        fields = ['description']
