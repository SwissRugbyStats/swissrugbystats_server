import graphene
from graphene_django.types import DjangoObjectType

from swissrugbystats.core.models import Game, GameParticipation


class GameType(DjangoObjectType):
    class Meta:
        model = Game


class GameParticipationType(DjangoObjectType):
    class Meta:
        model = GameParticipation


class Query(object):
    all_games = graphene.List(GameType)
    all_gameParticipations = graphene.List(GameParticipationType)

    def resolve_all_games(self, info, **kwargs):
        return Game.objects.all()

    def resolve_all_gameParticipations(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return GameParticipation.objects.select_related('game').all()
