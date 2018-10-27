# -*- coding: utf-8 -*-
import threading

from django.conf import settings
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from swissrugbystats.api.crawler.serializer import CrawlerLogMessageSerializer
from swissrugbystats.api.serializer import GameSerializer
from swissrugbystats.core.models import Season, Game, Competition
from swissrugbystats.crawler import tasks
from swissrugbystats.crawler.models import CrawlerLogMessage


def not_allowed_response():
    return Response({
        "Error": "You are not allowed to start the crawler. Please login with an account with according permissions."},
        status.HTTP_403_FORBIDDEN)


@api_view(['POST', 'GET'])
def start(request):
    """
    Start crawling.

    TODO:
    - Keep track of started crawls, or allow webhook param for callback.
    """
    if request.user.is_superuser:
        if request.method == 'POST':
            print("Crawler: start {}".format(request))

            deep = request.data.get('deep', False) == "True"
            season = request.data.get('season', settings.CURRENT_SEASON)
            async = request.data.get('async', False) == "True"

            t = threading.Thread(target=tasks.crawl_and_update, args=(deep, season, async))
            t.start()

            season_object = Season.objects.get(id=season)
            success_msg = "Crawler started in a separate thread for season {} and args deep_crawl={}, async={}. Check the crawler logs for results.".format(
                season_object, deep, async)
            crawler_logs_url = reverse('crawler-logs', request=request)

            return Response({"Success": {"info": success_msg, "goto": crawler_logs_url}}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"description": "Start the crawler by calling this endpoint via post.", "allowed_parameters": {
                    "deep": "boolean",
                    "season": "number",
                    "async": "boolean"

                }}, status.HTTP_200_OK)
    else:
        not_allowed_response()


@api_view(['POST', 'GET'])
def crawl_game(request, pk):
    """
    Crawl a game by id

    """
    if request.user.is_superuser:
        if request.method == 'POST':
            print("Crawler: crawl game {}".format(pk))

            try:
                tasks.crawl_game(pk)
            except Game.DoesNotExist as e:
                return Response({"Error": "There was an error. Game does not exist."}, status.HTTP_404_NOT_FOUND)

            game = Game.objects.get(pk=pk)

            return Response(GameSerializer(instance=game).data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"description": "Start the crawler by calling this endpoint via post."}, status.HTTP_200_OK)
    else:
        not_allowed_response()


@api_view(['POST', 'GET'])
def crawl_competition(request, pk):
    """
    Crawl a competition by id

    """
    if request.user.is_superuser:
        if request.method == 'POST':
            print("Crawler: crawl competition {}".format(pk))

            competitions = Competition.objects.filter(pk=pk)

            if not (competitions and len(competitions) > 0):
                return Response({"Error": "There was an error. Competition does not exist."}, status.HTTP_404_NOT_FOUND)

            deep = request.data.get('deep', False) == "True"
            season = competitions[0].season.id
            async = request.data.get('async', False) == "True"
            competition_filter = list(competitions)

            t = threading.Thread(target=tasks.crawl_and_update, args=(deep, season, async, competition_filter))
            t.start()

            season_object = Season.objects.get(id=season)
            success_msg = ("Crawler started in a separate thread for season {} "
                           "and args deep_crawl={}, async={} competition_filter={}."
                           "Check the crawler logs for results.").format(
                season_object, deep, async, competition_filter)
            crawler_logs_url = reverse('crawler-logs', request=request)

            return Response({"Success": {"info": success_msg, "goto": crawler_logs_url}}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"description": "Start the crawler by calling this endpoint via post."}, status.HTTP_200_OK)
    else:
        not_allowed_response()


class CrawlerLogMessageList(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    queryset = CrawlerLogMessage.objects.all()
    serializer_class = CrawlerLogMessageSerializer


class CrawlerLogMessageDetail(generics.RetrieveUpdateAPIView):
    """
    Todo: document.
    """
    queryset = CrawlerLogMessage.objects.all()
    serializer_class = CrawlerLogMessageSerializer
