from django.contrib import admin
from swissrugbystats.core.models import Association, Club, Competition, Team, Game, League, Venue, Referee, GameParticipation, Season, Favorite
from simple_history.admin import SimpleHistoryAdmin

# custom AdminModels


class ClubAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'get_associations', 'website')
    search_fields = ['name', 'abbreviation']
    list_filter = ['associations', ]


class CompetitionAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', )
    list_filter = ('league', 'season')


class GameAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'competition', 'venue')
    search_fields = ['host__team', 'guest__team', 'venue']
    list_filter = ['date', 'competition', 'competition__season', 'competition__league']


class GameParticipationAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'get_game')
    list_filter = ['team', 'hostTeam_set__competition', 'guestTeam_set__competition']


class FavoriteAdmin(SimpleHistoryAdmin):
    list_display = ('user', 'team')
    search_fields = ['user', 'team']


# Register your models here.

admin.site.register(Association, SimpleHistoryAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Team, SimpleHistoryAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(League, SimpleHistoryAdmin)
admin.site.register(Venue, SimpleHistoryAdmin)
admin.site.register(Referee, SimpleHistoryAdmin)
admin.site.register(GameParticipation, GameParticipationAdmin)
admin.site.register(Season, SimpleHistoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)