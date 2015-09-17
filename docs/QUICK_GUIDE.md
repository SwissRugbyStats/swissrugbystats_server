Quick User Guide
================

Crawling
--------

### Get updates for the current season
- create the leagues, seasons and competitions manually in the django-admin
- set the current season according to the created objects
- call `python manage.py crawl_and_update` to get the latest game updates
- or `python manage.py crawl_and_update --deep` to get updates on all the games of the season

### Get updates for a past season
- call `python manage.py crawl_and_update <season_id>` to get the latest game updates
- or `python manage.py crawl_and_update --deep <season_id>` to get updates on all the games of the season
 

Schedule Widget for your Website
--------------------------------
- include the srs-widget javascript file in your site:

    <script type='text/javascript' src='http://swissrugbystats.ch/lib/srs-widgets.js'></script>
    
- place a div in your site, wherever you want to display the schedule

    <div class="srs-schedule" data-teamid="45" data-seasonid="3">Schedule loading...</div>