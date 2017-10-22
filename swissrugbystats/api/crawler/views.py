# -*- coding: utf-8 -*-
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from swissrugbystats.api.crawler.serializer import CrawlerLogMessageSerializer
from swissrugbystats.crawler import tasks
from swissrugbystats.crawler.models import CrawlerLogMessage
from swissrugbystats.core.models import Season
import threading

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

            t = threading.Thread(target=tasks.update_all, args=(deep, season, async))
            t.start()

            season_object = Season.objects.get(id=season)
            success_msg = "Crawler started in a separate thread for season {} and args deep_crawl={}, async={}. Check the crawler logs for results.".format(season_object, deep, async)
            crawler_logs_url = reverse('crawler-logs', request=request)

            return Response({"Success": { "info": success_msg, "goto": crawler_logs_url }}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"description": "Start the crawler by calling this enpoint via post.", "allowed_parameters": {
                    "deep": "boolean",
                    "season": "number",
                    "async": "boolean"

            }}, status.HTTP_200_OK)
    else:
        return Response ({"Error": "You are not allowed to start the crawler. Please login with an account with according permissions."}, status.HTTP_403_FORBIDDEN)

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