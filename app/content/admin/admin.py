from django.contrib import admin

from app.content import models


admin.site.register(models.Event)
admin.site.register(models.News)
admin.site.register(models.Warning)
admin.site.register(models.Category)
admin.site.register(models.JobPost)
admin.site.register(models.User)


@admin.register(models.UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'is_on_wait', 'has_attended')