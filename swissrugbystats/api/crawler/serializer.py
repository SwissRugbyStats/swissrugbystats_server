from rest_framework import serializers
from swissrugbystats.crawler.models import CrawlerLogMessage

class CrawlerLogMessageSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        fields = '__all__'
        model = CrawlerLogMessage