from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from swissrugbystats.api import views

urlpatterns = [
    path(r'', views.api_root),
    path(r'swagger', views.schema_view),

    # get urls from sub modules
    path('', include('swissrugbystats.api.auth.urls')),
    path('', include('swissrugbystats.api.crawler.urls')),

    # re_path('config', views.ConfigurationVariableList.as_view(), name="config"),

    path('leagues', views.LeagueList.as_view(), name="leagues"),
    path('leagues/<int:pk>', views.LeagueDetail.as_view(), name='leagues_detail'),

    path('games', views.GameList.as_view(), name="games"),
    path('games/<int:pk>', views.GameDetail.as_view()),

    path('gameparticipations', views.GameParticipationList.as_view(), name="game-participations"),
    path('gameparticipations/<int:pk>', views.GameParticipationDetail.as_view()),

    path('clubs', views.ClubList.as_view(), name="clubs"),
    path('clubs/<int:pk>', views.ClubDetail.as_view()),

    path('teams', views.TeamList.as_view(), name="teams"),
    path('teams/<int:pk>', views.TeamDetail.as_view()),

    path('teams/<int:pk>/games', views.GameSchedule.as_view(), name="game-schedule"),
    path('teams/<int:pk>/games/next', views.NextGameByTeamId.as_view(), name="next-game"),
    path('teams/<int:pk>/games/last', views.LastGameByTeamId.as_view(), name="last-game"),
    path('teams/<int:pk>/games/season/<int:season>', views.get_team_games_by_season,
         name="last-game"),

    path('players', views.PlayerList.as_view(), name="players"),
    path('players/<int:pk>', views.PlayerDetail.as_view()),

    path('referees', views.RefereeList.as_view(), name="referees"),
    path('referees/<int:pk>', views.RefereeDetail.as_view()),

    path('seasons', views.SeasonList.as_view(), name="seasons"),

    path('competitions', views.CompetitionList.as_view(), name="competitions"),
    path('competitions/<int:pk>', views.CompetitionDetail.as_view(), name="competitions"),

    path('venues', views.VenueList.as_view(), name="venues"),
    path('venues/<int:pk>', views.VenueDetail.as_view()),

    path('users', views.CreateUser.as_view(), name='create-user'),
    # re_path('users/changePW$', views.CreateUser.as_view(), name='create-user'),
    path('favorites', views.CreateFavorite.as_view(), name='create-favorite'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
