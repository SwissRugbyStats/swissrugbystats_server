from django.contrib import admin
from swissrugbystats.core.models import Association, Club, Competition, Team, Game, League, Venue, Referee, GameParticipation, Season, Favorite
from simple_history.admin import SimpleHistoryAdmin

# custom AdminModels


class GameAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'competition', 'venue')
    search_fields = ['host__team', 'guest__team', 'venue']
    list_filter = ['date', 'competition', 'competition__season', 'competition__league']


class FavoriteAdmin(SimpleHistoryAdmin):
    list_display = ('user', 'team')
    search_fields = ['user', 'team']


# Register your models here.

admin.site.register(Association, SimpleHistoryAdmin)
admin.site.register(Club, SimpleHistoryAdmin)
admin.site.register(Competition, SimpleHistoryAdmin)
admin.site.register(Team, SimpleHistoryAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(League, SimpleHistoryAdmin)
admin.site.register(Venue, SimpleHistoryAdmin)
admin.site.register(Referee, SimpleHistoryAdmin)
admin.site.register(GameParticipation, SimpleHistoryAdmin)
admin.site.register(Season, SimpleHistoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)