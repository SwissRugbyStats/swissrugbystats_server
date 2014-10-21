from django.contrib import admin
from swissrugby.models import Team, Game, League

# Register your models here.

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)