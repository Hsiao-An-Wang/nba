import urllib.request as request
from bs4 import BeautifulSoup
import re
from pprint import pprint
import sqlite3


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == '__main__':

    base_url = 'http://espn.go.com'

    teams_url = 'http://espn.go.com/nba/teams'
    html_teams = request.urlopen(teams_url)

    soup_teams = BeautifulSoup(html_teams, 'lxml')

    urls = soup_teams.find_all(href=re.compile('/nba/teams/stats'))
    team_urls = [base_url + url['href'] for url in urls]

    team_url = 'http://espn.go.com/nba/team/stats/_/name/mil/milwaukee-bucks'
    html_team = request.urlopen(team_url)

    soup_team = BeautifulSoup(html_team, 'lxml')

    html_rows = soup_team.find_all('tr', class_=re.compile('player'))

    for row in html_rows:
        print(row.a['href'])

    for row in html_rows:
        print(row.a['href'].replace('_', 'stats/_'))

    player_urls = [row.a['href'].replace('_', 'stats/_') for row in html_rows]

    player_id = player_urls[0].split('/')[8]

    player_url = 'http://espn.go.com/nba/player/stats/_/id/3032977/Giannis Antetokounmpo'
    html_player = request.urlopen(player_url)

    soup_player = BeautifulSoup(html_player, 'lxml')

    soup_name = soup_player.find('meta', property='og:title')
    player_name = soup_name['content']

    regular_season_stats = soup_player.find_all('tr', class_=re.compile('row'))
    len(regular_season_stats)

    for stat in regular_season_stats:
        print(stat.get_text())
    size = int(len(regular_season_stats) / 3)  # LeBron's has participated in 12 seasons

    season_avgs_slice = slice(0, size)
    #season_totals_slice = slice(size, size * 2)
    #season_misc_totals_slice = slice(size * 2, size * 3)

    regular_season_avgs = regular_season_stats[season_avgs_slice]
    #regular_season_totals = regular_season_stats[season_totals_slice]
    #regular_season_misc_totals = regular_season_stats[season_misc_totals_slice]

    for stat in regular_season_avgs:
        print(stat.get_text())

    # for stat in regular_season_totals:
    #     print(stat.get_text())
    #
    # for stat in regular_season_misc_totals:
    #     print(stat.get_text())

    avgs = []
    for row in regular_season_avgs:
        for data in row:
            avgs.append(data.get_text())

    index = 0  # insert the player ID before the player's season
    increment = 0
    for row in range(len(regular_season_avgs)):
        avgs.insert(index + increment, player_id)
        index = index + 20  # There are 20 columns in the season avgs section
        increment = increment + 1

    index = 1  # insert the player's name after the player's ID
    increment = 0
    for row in range(len(regular_season_avgs)):
        avgs.insert(index + increment, player_name)
        index = index + 21  # There are 21 columns in the season avgs section since I've just added player ID
        increment = increment + 1

    # totals = []
    # for row in regular_season_totals:
    #     for data in row:
    #         totals.append(data.get_text())
    # index = 0  # insert the player ID before the player's season
    # increment = 0
    # for row in range(len(regular_season_totals)):
    #     totals.insert(index + increment, player_id)
    #     index = index + 17  # There are 17 columns in the reg season totals section
    #     increment = increment + 1
    # index = 1  # insert the player's name after the player's ID
    # increment = 0
    # for row in range(len(regular_season_totals)):
    #     totals.insert(index + increment, player_name)
    #     index = index + 18  # There are now 18 columns in the reg season totals after inserting player's ID
    #     increment = increment + 1
    #
    # # misc_totals
    # misc_totals = []
    # for row in regular_season_misc_totals:
    #     for data in row:
    #         misc_totals.append(data.get_text())
    # index = 0  # insert the player ID before the player's season
    # increment = 0
    # for row in range(len(regular_season_misc_totals)):
    #     misc_totals.insert(index + increment, player_id)
    #     index = index + 13  # There are 13 columns in the reg season misc totals section
    #     increment = increment + 1
    # index = 1  # insert the player's name after the player's ID
    # increment = 0
    # for row in range(len(regular_season_misc_totals)):
    #     misc_totals.insert(index + increment, player_name)
    #     index = index + 14  # There are now 14 columns in the reg season misc totals after inserting player ID
    #     increment = increment + 1
    print(avgs)
    conn = sqlite3.connect("C:\\Users\\Justin\\Desktop\\sqllite\\SQLiteStudio\\nba.db")
    c = conn.cursor()

    for row in chunks(avgs, 22):
        pprint(row)

    for row in chunks(avgs, 22):
        try:
            c.execute('INSERT INTO regular_season_avgs VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)
        except:
            pass
        conn.commit()
    conn.close()