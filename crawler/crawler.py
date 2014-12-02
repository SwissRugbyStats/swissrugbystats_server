import requests
from BeautifulSoup import BeautifulSoup

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

leagueResults = [(l, "http://www.suisserugby.com/competitions/" + l + "/lt/results.html") for l in leagues]
leagueTeams = [(l, "http://www.suisserugby.com/competitions/" + l + ".html") for l in leagues]
leagueFixtures = [(l, "http://www.suisserugby.com/competitions/" + l + "/lt/fixtures.html") for l in leagues]


def crawlLeagueResults(leagueResultsUrl):
    results = []
    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    for url in leagueResultsUrl:
        r = requests.get(url[1], headers=headers)
        soup = BeautifulSoup(r.text)
        data = []
        table = soup.find('table', attrs={'class': 'table'})

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) > 0:
                game = []
                game.append(cells[0].find(text=True))   # fsrID
                game.append(cells[0].find('a')['href']) # fsrUrl

                game.append(cells[1].find(text=True))   # date

                teams = cells[2].find(text=True)        # teams
                teams2 = teams.split(' - ')
                game.append(teams2[0].strip())
                game.append(teams2[1].strip())

                score = cells[3].find(text=True)        # scores
                score2 = score.split('-')
                game.append(score2[0].strip())
                game.append(score2[1].strip())

                data.append(game)
        results.append((url[0], data))
    return results

def crawlLeagueTeams(leagueUrl):
    teams = []

    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    for url in leagueUrl:
        r = requests.get(url[1], headers=headers)
        soup = BeautifulSoup(r.text)
        data = []
        table = soup.find('table', attrs={'class': 'table'})

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) > 0:
                # parse Teamname and remove leading and tailing spaces
                data.append(cells[1].find(text=True).strip())
        teams.append((url[0], data))

    return teams


def crawlLeagueFixtures(leagueFixturesUrl):
    fixtures = []
    headers = {
        'User-Agent': 'Mozilla 5.0'
    }
    for url in leagueFixturesUrl:
        r = requests.get(url[1], headers=headers)
        soup = BeautifulSoup(r.text)
        data = []
        table = soup.find('table', attrs={'class': 'table'})
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) > 0:
                teams = cells[2].find(text=True)        # teams
                teams2 = teams.split(' - ')

                fixture = [
                    cells[0].find('a').find(text=True), # fsrId
                    cells[0].find('a')['href'],         # fsrUrl
                    cells[1].find(text=True),           # date
                    teams2[0].strip(),                 # host
                    teams2[1].strip()                  # guest
                ]
                data.append(fixture)


        # recursively parse all next sites
        pagination = soup.find('div', attrs={'class': 'pagination'})
        current = int(pagination.find('span', attrs={'class': 'current'}).find(text=True))
        if current == 1:
            for page in pagination.findAll('a', attrs={'class': 'inactive'}):
                if int(page.find(text=True)) > current:
                    nextUrl = [("blubb", page['href'])]
                    x = crawlLeagueFixtures(nextUrl)
                    data+x

        fixtures.append((url[0], data))

    return fixtures

'''
print "Teams:\n"

#print str(crawlLeagueTeams(leagues))


print "\n------------------\n"

print "League Scores:\n"

#print str(crawlLeagueResults(leagues))

print "\n------------------\n"

print "League Fixtures:\n"
'''
#print str(crawlLeagueFixtures(leagueFixtures))