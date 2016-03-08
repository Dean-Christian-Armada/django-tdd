from django.contrib import admin
from .models import Poll, Choice

# Register your models here.
class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 3

class PollAdmin(admin.ModelAdmin):
	inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)