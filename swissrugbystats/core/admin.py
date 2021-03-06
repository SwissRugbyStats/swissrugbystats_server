# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from swissrugbystats.core.models import Association, Club, Competition, Team, Game, League, Venue, Referee, \
    GameParticipation, Season, Favorite


# custom AdminModels


class TeamAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'club', 'current_competition')
    search_fields = ['name', 'club__name']
    list_filter = ['club', 'current_competition']


class ClubAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'get_associations', 'website')
    search_fields = ['name', 'abbreviation']
    list_filter = ['associations', ]


class CompetitionAdmin(SimpleHistoryAdmin):
    list_display = ('__str__',)
    list_filter = ('league', 'season')


class GameAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'date', 'competition', 'venue')
    search_fields = ['host__team', 'guest__team__name', 'venue__name']
    list_filter = ['date', 'competition', 'competition__season', 'competition__league']


class GameParticipationAdmin(SimpleHistoryAdmin):
    list_display = ['__str__', 'get_game', 'forfait']
    list_filter = ['team', 'forfait', 'hostTeam_set__competition', 'guestTeam_set__competition']


class FavoriteAdmin(SimpleHistoryAdmin):
    list_display = ['user', 'team']
    search_fields = ['user', 'team__name']


class LeagueAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'shortcode', 'description', 'archived']
    list_editable = ['shortcode', 'archived']
    list_filter = ['archived']
    search_fields = ['name', 'shortcode', 'description']


# Register your models here.

admin.site.register(Association, SimpleHistoryAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Venue, SimpleHistoryAdmin)
admin.site.register(Referee, SimpleHistoryAdmin)
admin.site.register(GameParticipation, GameParticipationAdmin)
admin.site.register(Season, SimpleHistoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)
