from django.contrib import admin
from swissrugby.models import Team, Game, League, Venue, Referee, GameParticipation

# Register your models here.

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(Venue)
admin.site.register(Referee)
admin.site.register(GameParticipation)