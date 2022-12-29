from django.contrib import admin
from solo.admin import SingletonModelAdmin
from notes_site.models import (
    Note,
    Authorize,
    Registration,
    MailSettings,
    Tags
    )   


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    class Meta:
        model = Note
        fields = [ "title","description ", "posted_date"]


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


@admin.register(MailSettings)
class MailSettingsAdmin(SingletonModelAdmin):
    class Meta:
        model = MailSettings
        fields = ['domen','title','description']

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    class Meta:
        model = Tags
        fields = ['note','tag']