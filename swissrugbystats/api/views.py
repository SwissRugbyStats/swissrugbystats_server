from swissrugbystats.core.models import *
from swissrugbystats.api.serializer import *
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_admin_conf_vars.models import ConfigurationVariable
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from swissrugbystats.api.http_errors import ResourceAlreadyExists
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import filters

@api_view(('GET',))
def api_root(request, format=None):
    """
    Todo: complete available urls
    Feel free to use this API. I would love to see what you did with it.
    """
    return Response({
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
            "{}/<id>".format(reverse('game-participations', request=request, format=format)): 'game-participations detail',
        },
        '/clubs': {
            reverse('clubs', request=request, format=format): 'list of all clubs',
            "{}/<id>".format(reverse('clubs', request=request, format=format)): 'club detail',
        },
        '/config': 'list of all config',
        '/teams': {
            reverse('teams', request=request, format=format): 'list of all teams',
            "{}/<team-id>".format(reverse('teams', request=request, format=format)): {
                "{}/<team-id>".format(reverse('teams', request=request, format=format)): 'team-details',
                "{}/<team-id>/games".format(reverse('teams', request=request, format=format)): {
                    "{}/<team-id>/games".format(reverse('teams', request=request, format=format)): 'all games by team-id',
                    "{}/<team-id>/games/season/<season-id>".format(reverse('teams', request=request, format=format)): 'all games by team and season id',
                    "{}/<team-id>/games/next".format(reverse('teams', request=request, format=format)): 'next game',
                    "{}/<team-id>/games/last".format(reverse('teams', request=request, format=format)): 'last game',
                }
            }
        },
        '/players': {
            '/': reverse('players', request=request, format=format),
            '/{id}' : 'player details'
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
        }
    })


class ConfigurationVariableList(generics.ListAPIView):
    """
    Get a list of all configuration variables.
    Only visible to authenticated users.
    """

    queryset = ConfigurationVariable.objects.all()
    serializer_class = ConfigurationVariableSerializer


class LeagueList(generics.ListAPIView):
    """
    Get a list of all the leagues.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


# League detail
class LeagueDetail(generics.RetrieveAPIView):
    """
    Get details about a special league.
    """
    queryset = League.objects.all()
    serializer_class = LeagueDetailSerializer


class ClubList(generics.ListAPIView):
    """
    Get a list of all the clubs.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class ClubDetail(generics.RetrieveAPIView):
    """
    Get details about a special club.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class PlayerList(generics.ListAPIView):
    """
    Get a list of all the players.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['last_name', 'first_name']
    ordering = ['last_name', 'first_name']


class PlayerDetail(generics.RetrieveAPIView):
    """
    Get details about a special player.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class CompetitionList(generics.ListAPIView):
    """
    Get a list of all the competitions.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class GameList(generics.ListAPIView):
    """
    Todo: document.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetail(generics.RetrieveAPIView):
    """
    Todo: document.
    """
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer


class GameParticipationList(generics.ListAPIView):
    """
    Todo: document.
    """
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


class GameParticipationDetail(generics.RetrieveAPIView):
    """
    Todo: document.
    """
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


class TeamList(generics.ListAPIView):
    """
    Todo: document.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class TeamDetail(generics.RetrieveAPIView):
    """
    Todo: document.
    """
    queryset = Team.objects.all()
    serializer_class = TeamInsightSerializer


class GameSchedule(generics.ListAPIView):
    """
    Todo: document.
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


class RefereeList(generics.ListAPIView):
    """
    Todo: document.
    """
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class RefereeDetail(generics.RetrieveAPIView):
    """
    Todo: document.
    """
    queryset = Referee.objects.all()
    serializer_class = VenueSerializer


class VenueList(generics.ListAPIView):
    """
    Todo: document.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class VenueDetail(generics.RetrieveAPIView):
    """
    Todo: document.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class SeasonList(generics.ListAPIView):
    """
    Todo: document.
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class NextGameByTeamId(generics.RetrieveAPIView):
    """
    Todo: document.
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


class LastGameByTeamId(generics.RetrieveAPIView):
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
    permission_classes = (permissions.AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        u_email = serializer.data['username']
        if u_email is not None:
            VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
            serialized = UserSerializer(data=self.request.DATA)
            if serialized.is_valid():
                user_data = {field: data for (field, data) in self.request.DATA.items() if field in VALID_USER_FIELDS}
                user_data.update(email=u_email)
                user = get_user_model().objects.create_user(
                    **user_data
                )
                text = 'Thanks for registering on swissrugbystats.ch! You can now log in and add your favorite teams.'
                send_mail('Thanks for registering', text, 'christian.glatthard@rugbygear.ch', [u_email], fail_silently=False)
                return Response(UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class CreateFavorite(generics.ListCreateAPIView):
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
        #f = Favorite(team=t, user=u)
        favs = Favorite.objects.filter(team=t, user=u)
        if len(favs) > 0:
            raise ResourceAlreadyExists()
        f = Favorite(team=t, user=u)
        f.save()