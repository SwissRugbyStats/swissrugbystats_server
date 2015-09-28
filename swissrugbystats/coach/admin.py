from django.contrib import admin
from swissrugbystats.coach.models import TrophyType, Trophy, Position, LineUp, LineUpPosition, Card, CardType, Point, PointType, Player
from simple_history.admin import SimpleHistoryAdmin

# custom AdminModels
"""
class ClubAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'get_associations', 'website')
    search_fields = ['name', 'abbreviation']
    list_filter = ['associations', ]
"""


# Register your models here.

admin.site.register(Player, SimpleHistoryAdmin)
admin.site.register(TrophyType, SimpleHistoryAdmin)
admin.site.register(Trophy, SimpleHistoryAdmin)
#admin.site.register(LineUp, SimpleHistoryAdmin)
#admin.site.register(LineUpPosition, SimpleHistoryAdmin)
admin.site.register(PointType, SimpleHistoryAdmin)
admin.site.register(Point, SimpleHistoryAdmin)
admin.site.register(Position, SimpleHistoryAdmin)
admin.site.register(CardType, SimpleHistoryAdmin)
admin.site.register(Card, SimpleHistoryAdmin)