# -*- coding: utf-8 -*-
from django.contrib import admin
from swissrugbystats.coach.models import TrophyType, Trophy, Position, LineUp, LineUpPosition, Card, CardType, Point, PointType, Player
from simple_history.admin import SimpleHistoryAdmin

# custom AdminModels


class PlayerAdmin(SimpleHistoryAdmin):
    list_display = ('get_full_name', 'club', 'birth_date')
    search_fields = ['get_full_name']
    list_filter = ['club']

"""
class ClubAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'get_associations', 'website')
    search_fields = ['name', 'abbreviation']
    list_filter = ['associations', ]
"""


# Register your models here.

admin.site.register(Player, PlayerAdmin)
admin.site.register(TrophyType, SimpleHistoryAdmin)
admin.site.register(Trophy, SimpleHistoryAdmin)
#admin.site.register(LineUp, SimpleHistoryAdmin)
#admin.site.register(LineUpPosition, SimpleHistoryAdmin)
admin.site.register(PointType, SimpleHistoryAdmin)
admin.site.register(Point, SimpleHistoryAdmin)
admin.site.register(Position, SimpleHistoryAdmin)
admin.site.register(CardType, SimpleHistoryAdmin)
admin.site.register(Card, SimpleHistoryAdmin)