__author__ = 'chregi'

from django_admin_conf_vars.global_vars import config

config.set("CURRENT_SEASON", default=1)
config.set("COMPETITIONS_BASE_URL", default="http://www.suisserugby.com/competitions/")
config.set("ARCHIVE_BASE_URL", default="http://www.suisserugby.com/competitions/archiv/")
config.set("FIXTURES_URL_ENDING", default="/lt/fixtures.html")
config.set("RESULTS_URL_ENDING", default="/lt/results.html")
config.set("LEAGUE_URL_ENDING", default=".html")
