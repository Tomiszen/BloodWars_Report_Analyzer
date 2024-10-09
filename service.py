import model
import requests
from bs4 import BeautifulSoup
import re


def create_report_object(url, report_type):
    return model.Report(url, "Arena klanowa")


def make_soup(report):
    r = requests.get(report.url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.find_all("div", class_="msg-notBattleReport"))
        if soup.find_all("div", class_="msg-notBattleReport"):
            return False
        else:
            return soup
    else:
        return False


def get_opponents(soup, report):
    report.set_attacker(soup.find('td', {'class': 'attacker'}).text)
    report.set_defender(soup.find('td', {'class': 'defender'}).text)


def get_players(soup, side, clan):
    if side == 'attacker':
        players_soup = soup.find('div', {'class': 'amblist rlr fll'})
    else:
        players_soup = soup.find('div', {'class': 'amblist rll flr'})
    players_soup = players_soup.find_all('span')
    read_players(players_soup, clan)


def read_players(soup, clan):
    for player in soup:
        player_id = re.findall("[a-z]{2}_[0-9]+", str(player))[0]
        name = player.text.strip()
        model.Player(player_id, name, clan)


