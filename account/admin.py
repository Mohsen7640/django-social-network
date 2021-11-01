from django.contrib import admin

from account.models import Profile, Relationship


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass
