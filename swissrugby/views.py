from swissrugby.models import League, Game, Team, GameParticipation, Referee, Venue, Season
from swissrugby.serializer import LeagueSerializer, GameSerializer, TeamSerializer, GameParticipationSerializer, TeamInsightSerializer, RefereeSerializer, VenueSerializer, SeasonSerializer, GameDetailSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail

''' --------------------------------

    API

-------------------------------- '''

# API root
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'leagues': reverse('leagues', request=request, format=format),
        'games': reverse('games', request=request, format=format),
        'game-participations': reverse('game-participations', request=request, format=format),
        'teams': reverse('teams', request=request, format=format),
        'referees': reverse('referees', request=request, format=format),
        'seasons': reverse('seasons', request=request, format=format),
        'venues': reverse('venues', request=request, format=format)
    })

# League list
class LeagueList(generics.ListAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

# League detail
class LeagueDetail(generics.RetrieveAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


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
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        u_email = serializer.data['username']
        if u_email is not None:
            serializer.save(email=u_email, is_active=False)
            send_mail('Thanks for registering', 'Here is the message.', 'chregi.glatthard@gmail.com', [u_email], fail_silently=False)



