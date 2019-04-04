from datetime import datetime

from swissrugbystats import settings
from swissrugbystats.core.models import Season


class SeasonManager(object):

    @staticmethod
    def get_current_season() -> Season:
        """
        Return the current season or create it if not existing yet.
        :return:
        """

        today = datetime.now()
        year_today = today.year
        month_today = today.month

        season_year_start = year_today

        # if the current month is before september,
        # this means we're in the second half of last years season
        if month_today < 8:
            season_year_start = season_year_start - 1

        name = "{}{}".format(season_year_start, settings.SEASON_NAME_SEPARATOR, season_year_start + 1)
        fsr_url_slug = "{}{}".format(settings.SEASON_FSR_SLUG_PREFIX, name)

        matching_season = Season.objects.filter(fsr_url_slug=fsr_url_slug)

        if len(matching_season) > 0:
            s = matching_season[0]
        else:
            s = Season()
            s.fsr_url_slug = fsr_url_slug
        s.is_current = True
        s.name = name
        s.save()
        return s
