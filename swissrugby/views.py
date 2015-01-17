from swissrugby.models import League, Game, Team, GameParticipation, Referee, Venue, Season, Favorite
from swissrugby.serializer import LeagueSerializer, GameSerializer, TeamSerializer, GameParticipationSerializer, TeamInsightSerializer, RefereeSerializer, VenueSerializer, SeasonSerializer, GameDetailSerializer, UserSerializer, FavoriteSerializer, FavoriteDetailSerializer, LeagueDetailSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from http_errors import ResourceAlreadyExists
from django.contrib.auth import get_user_model
from rest_framework import status

''' --------------------------------

    API

-------------------------------- '''

'''
API Root
'''
@api_view(('GET',))
def api_root(request, format=None):
    '''
    Feel free to use this API. I would love to see what you did with it.
    '''
    return Response({
        'leagues': reverse('leagues', request=request, format=format),
        'games': reverse('games', request=request, format=format),
        'game-participations': reverse('game-participations', request=request, format=format),
        'teams': reverse('teams', request=request, format=format),
        'referees': reverse('referees', request=request, format=format),
        'seasons': reverse('seasons', request=request, format=format),
        'venues': reverse('venues', request=request, format=format)
    })


class LeagueList(generics.ListAPIView):
    '''
    Get a list of all the leagues.
    '''
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


# League detail
class LeagueDetail(generics.RetrieveAPIView):
    '''
    Get details about a special league.
    '''
    queryset = League.objects.all()
    serializer_class = LeagueDetailSerializer


# Game list
class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# Game detail
class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer



# GameParticipation list
class GameParticipationList(generics.ListAPIView):
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


# GameDetail detail
class GameParticipationDetail(generics.RetrieveAPIView):
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


# Team list
class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


# Team detail
class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamInsightSerializer


# Referee list
class RefereeList(generics.ListAPIView):
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer

# Referee detail
class RefereeDetail(generics.RetrieveAPIView):
    queryset = Referee.objects.all()
    serializer_class = VenueSerializer

# Venue list
class VenueList(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

# Venue detail
class VenueDetail(generics.RetrieveAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

# Season list
class SeasonList(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class NextGameByTeamId(generics.RetrieveAPIView):
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

        return obj.getNextGame()


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

        return obj.getLastGame()


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