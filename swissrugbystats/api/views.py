# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from swissrugbystats.api.http_errors import ResourceAlreadyExists
from swissrugbystats.api.serializer import *


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, CoreJSONRenderer])
def schema_view(request):
    '''
    Swagger Documentation of the Swiss Rugby Stats API.
    :param request:
    :return:
    '''
    generator = schemas.SchemaGenerator(title='Swiss Rugby Stats API', urlconf='swissrugbystats.api.urls')
    return response.Response(generator.get_schema(request=request))


@api_view(('GET',))
def api_root(request, format=None):
    """
    Todo: complete available urls
    Feel free to use this API. I would love to see what you did with it.
    """
    return Response({
        '/swagger': 'A swagger UI of the API',
        '/leagues': {
            reverse('leagues', request=request, format=format): 'list of all league objects',
            "{}/<id>".format(reverse('leagues', request=request, format=format)): 'league details'
        },
        '/games': {
            reverse('games', request=request, format=format): 'list of all games',
            "{}/<id>".format(reverse('games', request=request, format=format)): 'game details',
        },
        '/game-participations': {
            reverse('game-participations', request=request, format=format): 'list of all game-participations',
            "{}/<id>".format(
                reverse('game-participations', request=request, format=format)): 'game-participations detail',
        },
        '/clubs': {
            reverse('clubs', request=request, format=format): 'list of all clubs',
            "{}/<id>".format(reverse('clubs', request=request, format=format)): 'club detail',
        },
        '/teams': {
            reverse('teams', request=request, format=format): 'list of all teams',
            "{}/<team-id>".format(reverse('teams', request=request, format=format)): {
                "{}/<team-id>".format(reverse('teams', request=request, format=format)): 'team-details',
                "{}/<team-id>/games".format(reverse('teams', request=request, format=format)): {
                    "{}/<team-id>/games".format(
                        reverse('teams', request=request, format=format)): 'all games by team-id',
                    "{}/<team-id>/games/season/<season-id>".format(
                        reverse('teams', request=request, format=format)): 'all games by team and season id',
                    "{}/<team-id>/games/next".format(reverse('teams', request=request, format=format)): 'next game',
                    "{}/<team-id>/games/last".format(reverse('teams', request=request, format=format)): 'last game',
                }
            }
        },
        '/players': {
            '/': reverse('players', request=request, format=format),
            '/{id}': 'player details'
        },
        '/referees': {
            '/': reverse('referees', request=request, format=format),
            '/{id}': 'referee details'
        },
        '/seasons': {
            '/': reverse('seasons', request=request, format=format),
            '/{id}': 'season details'
        },
        '/venues': {
            '/': reverse('venues', request=request, format=format),
            '/{id}': 'venue details'
        },
        '/competitions': {
            '/': reverse('competitions', request=request, format=format),
        },
        '/crawler': {
            '/start': reverse('crawler-start', request=request, format=format),
            '/logs': {
                '/': reverse('crawler-logs', request=request, format=format),
                '/{id}': 'crawler log details'
            }

        }
    })


class LeagueList(generics.ListCreateAPIView):
    """
    Get a list of all the leagues.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    ordering = ['name']


# League detail
class LeagueDetail(generics.RetrieveUpdateAPIView):
    """
    Get details about a special league.
    """
    queryset = League.objects.all()
    serializer_class = LeagueDetailSerializer


class ClubList(generics.ListCreateAPIView):
    """
    Get a list of all the clubs.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    ordering = ['name']


class ClubDetail(generics.RetrieveUpdateAPIView):
    """
    Get details about a special club.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class PlayerList(generics.ListCreateAPIView):
    """
    Get a list of all the players.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_fields = ['last_name', 'first_name']
    ordering = ['last_name', 'first_name']


class PlayerDetail(generics.RetrieveUpdateAPIView):
    """
    Get details about a special player.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class CompetitionList(generics.ListCreateAPIView):
    """
    Get a list of all the competitions.
    You can filter the list by using the query parameters.
    i.e.
    ...?league=1&season=3
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    filter_fields = ['season', 'league']


class CompetitionDetail(generics.RetrieveUpdateAPIView):
    """
    Get a competition.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class GameList(generics.ListCreateAPIView):
    """
    Get a list of all the games.
    You can filter by competition.
    """
    queryset = Game.objects.all()
    filter_fields = ['competition']
    serializer_class = GameSerializer


class GameDetail(generics.RetrieveUpdateAPIView):
    """
    Get details of a specific game.
    """
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer


class GameParticipationList(generics.ListCreateAPIView):
    """
    Get all the game participations.
    """
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


class GameParticipationDetail(generics.RetrieveUpdateAPIView):
    """
    Get details of a specific game participation.
    """
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


class TeamList(generics.ListCreateAPIView):
    """
    Get a list of all the teams.
    You can filter by name, club and current competition.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_fields = ['name', 'club', 'current_competition']
    ordering = ['name']


class TeamDetail(generics.RetrieveUpdateAPIView):
    """
    Get details of a specific team.
    """
    queryset = Team.objects.all()
    serializer_class = TeamInsightSerializer


class GameSchedule(generics.ListCreateAPIView):
    """
    Get the game schedule of a specific team.
    """
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = Team.objects.all()

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj.get_games()


class RefereeList(generics.ListCreateAPIView):
    """
    Get a list of all the referees.
    """
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer
    filter_fields = ['name']
    ordering = ['name']


class RefereeDetail(generics.RetrieveUpdateAPIView):
    """
    Get the details of a referee.
    """
    queryset = Referee.objects.all()
    serializer_class = VenueSerializer


class VenueList(generics.ListCreateAPIView):
    """
    Get a list of all the venues.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    ordering = ['name']


class VenueDetail(generics.RetrieveUpdateAPIView):
    """
    Get the details of a specific venue.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class SeasonList(generics.ListCreateAPIView):
    """
    Get a list of all the seasons.
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    ordering = ['name']


class NextGameByTeamId(generics.RetrieveUpdateAPIView):
    """
    Get the next game of a specific team.
    """
    queryset = Team.objects.all()
    serializer_class = GameSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj.get_next_game()


class LastGameByTeamId(generics.RetrieveUpdateAPIView):
    """
    Get the last game played by a specific team.
    """
    queryset = Team.objects.all()
    serializer_class = GameSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj.get_last_game()


@api_view(['GET'])
def get_team_games_by_season(request, pk, season):
    """
    Get all the games a team has in a specific season.
    :param request:
    :param pk:
    :param season:
    :return:
    """
    team = Team.objects.get(id=pk)
    games = team.get_games_by_season(season)
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUser(generics.CreateAPIView):
    """
    Create a user.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        u_email = serializer.data['username']
        if u_email is not None:
            VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
            serialized = UserSerializer(data=self.request.data)
            if serialized.is_valid():
                user_data = {field: data for (field, data) in self.request.data.items() if field in VALID_USER_FIELDS}
                user_data.update(email=u_email)
                user = get_user_model().objects.create_user(
                    **user_data
                )
                text = 'Thanks for registering on swissrugbystats.ch! You can now log in and add your favorite teams.'
                send_mail('Thanks for registering', text, 'christian.glatthard@rugbygear.ch', [u_email],
                          fail_silently=False)
                return Response(UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class CreateFavorite(generics.ListCreateAPIView):
    """
    Create a favourite.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FavoriteSerializer
        elif self.request.method == "GET":
            return FavoriteDetailSerializer

    def perform_create(self, serializer):
        u = self.request.user
        tid = serializer.data['team']
        t = Team.objects.get(id=tid)
        # f = Favorite(team=t, user=u)
        favs = Favorite.objects.filter(team=t, user=u)
        if len(favs) > 0:
            raise ResourceAlreadyExists()
        f = Favorite(team=t, user=u)
        f.save()
