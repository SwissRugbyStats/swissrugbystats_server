from django.contrib import admin
from swissrugby.models import Team, Game, League, Venue, Referee, GameParticipation, Season, Favorite

# custom AdminModels


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')
    search_fields = ['user', 'team']


# Register your models here.

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(Venue)
admin.site.register(Referee)
admin.site.register(GameParticipation)
admin.site.register(Season)
admin.site.register(Favorite, FavoriteAdmin)