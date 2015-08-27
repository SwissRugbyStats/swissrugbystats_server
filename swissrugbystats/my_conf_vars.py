__author__ = 'chregi'

from django_admin_conf_vars.global_vars import config

config.set("CURRENT_SEASON", default=1)
config.set("COMPETITIONS_BASE_URL", default="http://www.suisserugby.com/competitions/")
config.set("ARCHIVE_BASE_URL", default="http://www.suisserugby.com/competitions/archiv/")
config.set("FIXTURES_URL_ENDING", default="/lt/fixtures.html")
config.set("RESULTS_URL_ENDING", default="/lt/results.html")
config.set("LEAGUE_URL_ENDING", default=".html")


def get_league_url(league):
    return "{}{}{}".format(config.COMPETITIONS_BASE_URL, league, config.LEAGUE_URL_ENDING)


def get_fixtures_url(league):
    return "{}{}{}".format(config.COMPETITIONS_BASE_URL, league, config.FIXTURES_URL_ENDING)


def get_results_url(league):
    return "{}{}{}".format(config.COMPETITIONS_BASE_URL, league, config.RESULTS_URL_ENDING)


def get_archive_league_url(league, season_slug):
    return "{}{}/{}{}".format(config.ARCHIVE_BASE_URL, season_slug, league, config.LEAGUE_URL_ENDING)


def get_archive_fixtures_url(league, season_slug):
    return "{}{}/{}{}".format(config.ARCHIVE_BASE_URL, season_slug, league, config.FIXTURES_URL_ENDING)


def get_archive_results_url(league, season_slug):
    return "{}{}/{}{}".format(config.ARCHIVE_BASE_URL, season_slug, league, config.RESULTS_URL_ENDING)