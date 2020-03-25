import graphene
from graphene_django.types import DjangoObjectType

from swissrugbystats.core.models import Game, GameParticipation, Team, Club


class GameType(DjangoObjectType):
    class Meta:
        model = Game


class GameParticipationType(DjangoObjectType):
    class Meta:
        model = GameParticipation


class TeamType(DjangoObjectType):
    class Meta:
        model = Team


class ClubType(DjangoObjectType):
    class Meta:
        model = Club


class Query(object):
    all_games = graphene.List(GameType)
    all_game_participations = graphene.List(GameParticipationType)
    team = graphene.Field(TeamType,
                          id=graphene.Int(),
                          name=graphene.String())

    all_teams = graphene.List(TeamType)
    all_clubs = graphene.List(ClubType)

    def resolve_all_games(self, info, **kwargs):
        return Game.objects.all()

    def resolve_all_game_participations(self, info, **kwargs):
        return GameParticipation.objects.select_related('team').all()

    def resolve_team(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Team.objects.get(pk=id)

        if name is not None:
            return Team.objects.get(name=name)

        return None

    def resolve_all_teams(self, info, **kwargs):
        return Team.objects.select_related('club').all()

    def resolve_all_clubs(self, info, **kwargs):
        return Club.objects.all()
