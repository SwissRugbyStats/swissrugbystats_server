import requests, json
from BeautifulSoup import BeautifulSoup

__author__ = 'chregi'


def crawlLeagueResults(url):
    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    r = requests.get(url[1], headers=headers)
    soup = BeautifulSoup(r.text)
    data = []
    table = soup.find('table', attrs={'class': 'table'})

    for row in table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            game = []
            game.append(cells[0].find(text=True))
            game.append(cells[0].find('a')['href'])

            teams = cells[2].find(text=True)
            teams2 = teams.split('-')
            game.append(teams2[0].rstrip())
            game.append(teams2[1].lstrip())

            score = cells[3].find(text=True)
            score2 = score.split('-')
            game.append(score2[0].rstrip())
            game.append(score2[1].lstrip())

            data.append(game)
            #cols = [ele.text.strip() for ele in cols]
            #data.append([ele for ele in cols if ele]) # Get rid of empty values
    return url[0], data

def crawlLeagueTeams(url):
    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    r = requests.get(url[1], headers=headers)
    soup = BeautifulSoup(r.text)
    data = []
    table = soup.find('table', attrs={'class': 'table'})

    for row in table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            data.append(cells[1].find(text=True))
    return url[0], data


def crawlLeagueFixtures(url):
    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    r = requests.get(url[1], headers=headers)
    soup = BeautifulSoup(r.text)
    data = []
    table = soup.find('table', attrs={'class': 'table'})
    for row in table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            fixture = []
            fixture.append(cells[0].find('a').find(text=True))
            fixture.append(cells[0].find('a')['href'])
            fixture.append(cells[1].find(text=True))
            fixture.append(cells[2].find(text=True))
            data.append(fixture)


    # recursively parse all next sites
    pagination = soup.find('div', attrs={'class': 'pagination'})
    current = int(pagination.find('span', attrs={'class': 'current'}).find(text=True))
    if current == 1:
        for page in pagination.findAll('a', attrs={'class': 'inactive'}):
            if int(page.find(text=True)) > current:
                nextUrl = "blubb", page['href']
                x = crawlLeagueFixtures(nextUrl)
                data+x[1]

    return url[0], data


leagues = [
    "u16-east",
    "u16-west",
    "u18",
    "league-1-east",
    "league-1-west",
    "lnc-east",
    "lnc-west",
    "lnb",
    "lna"
]

leagueScores = [(l, "http://www.suisserugby.com/competitions/" + l + "/lt/results.html") for l in leagues]
leagueTeams = [(l, "http://www.suisserugby.com/competitions/" + l + ".html") for l in leagues]
leagueFixtures = [(l, "http://www.suisserugby.com/competitions/" + l + "/lt/fixtures.html") for l in leagues]


print "Teams:\n"

for url in leagueTeams:
    teams = str(crawlLeagueTeams(url))
    file = open("teams.txt", "w")
    file.write(teams)
    file.close()
    print teams

print "\n------------------\n"

print "League Scores:\n"
for url in leagueScores:
    scores = str(crawlLeagueResults(url))
    file = open("scores.txt", "w")
    file.write(scores)
    file.close()
    print scores


print "\n------------------\n"

print "League Fixtures:\n"
for url in leagueFixtures:
    fixtures = str(crawlLeagueFixtures(url))
    file = open("fixtures.txt", "w")
    file.write(fixtures)
    file.close()
    print fixtures
