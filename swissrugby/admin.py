from django.contrib import admin
from swissrugby.models import Team, Game, League, Venue, Referee, GameParticipation, Season, Favorite
from simple_history.admin import SimpleHistoryAdmin

# custom AdminModels


class GameAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'season', 'league', 'venue')
    search_fields = ['host__team', 'guest__team', 'venue']
    list_filter = ['season', 'date', 'league', 'venue']


class FavoriteAdmin(SimpleHistoryAdmin):
    list_display = ('user', 'team')
    search_fields = ['user', 'team']


# Register your models here.

admin.site.register(Team, SimpleHistoryAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(League, SimpleHistoryAdmin)
admin.site.register(Venue, SimpleHistoryAdmin)
admin.site.register(Referee, SimpleHistoryAdmin)
admin.site.register(GameParticipation, SimpleHistoryAdmin)
admin.site.register(Season, SimpleHistoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)