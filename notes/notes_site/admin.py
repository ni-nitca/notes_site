from django.contrib import admin
from solo.admin import SingletonModelAdmin
from notes_site.models import Note, Authorize, Registration


class NoteAdmin(admin.ModelAdmin):
    class Meta:
        model = Note
        fields = ["title", "description ", "posted_date","tags"]

class AuthorizeAdmin(SingletonModelAdmin):
    class Meta:
        model = Authorize
        fields = ['description']

class RegisterAdmin(SingletonModelAdmin):
    class Meta:
        model = Registration
        fields = ['description']

admin.site.register(Note, NoteAdmin)
admin.site.register(Authorize, AuthorizeAdmin)
admin.site.register(Registration, RegisterAdmin)
