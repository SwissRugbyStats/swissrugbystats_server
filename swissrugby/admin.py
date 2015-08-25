from django.contrib import admin
from swissrugby.models import Team, Game, League, Venue, Referee, GameParticipation, Season, Favorite

# custom AdminModels


class GameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'season', 'league', 'venue')
    search_fields = ['host__team', 'guest__team', 'venue']
    list_filter = ['season', 'date', 'league', 'venue']


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')
    search_fields = ['user', 'team']


# Register your models here.

admin.site.register(Team)
admin.site.register(Game, GameAdmin)
admin.site.register(League)
admin.site.register(Venue)
admin.site.register(Referee)
admin.site.register(GameParticipation)
admin.site.register(Season)
admin.site.register(Favorite, FavoriteAdmin)