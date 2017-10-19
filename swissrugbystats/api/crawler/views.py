# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from swissrugbystats.crawler import tasks
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

            deep = request.data.get('deep', False)
            season = request.data.get('season', settings.CURRENT_SEASON)
            t = threading.Thread(target=tasks.update_all, args=(deep, season))
            t.start()

            return Response({"Success": {"Crawler started"}}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"description": "Start the crawler by calling this enpoint via post.", "allowed_parameters": {
                    "deep": "boolean",
                    "season": "number"
                }}, status.HTTP_200_OK)
    else:
        return Response ({"Error": "You are not allowed to start the crawler."}, status.HTTP_403_FORBIDDEN)

