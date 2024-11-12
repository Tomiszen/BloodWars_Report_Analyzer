import model
import requests
from bs4 import BeautifulSoup
import re


def list_to_dictionary(list_to_convert):
    return {item.split(' poz. ')[0]: int(item.split(' poz. ')[1]) for item in list_to_convert}


def create_report_object(url, report_type):
    return model.Report(url, "Arena klanowa")


def make_soup(report):
    r = requests.get(report.url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.find_all("div", class_="msg-notBattleReport"):
            return False
        else:
            return soup
    else:
        return False


def read_opponents(soup):
    attacker = soup.find("td", {"class": "attacker"}).text
    defender = soup.find("td", {"class": "defender"}).text
    return {"attacker": attacker, "defender": defender}


def read_winner(soup):
    message = soup.find_all("div", {"class": "msg-quest"})[1]
    winner = message.find("b").text
    return winner


def get_players(soup, side, clan):
    if side == 'attacker':
        players_soup = soup.find('div', {'class': 'amblist rlr fll'})
    else:
        players_soup = soup.find('div', {'class': 'amblist rll flr'})
    players_soup = players_soup.find_all('span')
    read_players(players_soup, clan)


def read_players(soup, clan):
    for player in soup:
        player_id = read_player_id(player)
        name = read_player_name(player)
        player_obj = model.Player(player_id, name, clan)
        read_info_from_onmouseover(player, player_obj)


def read_player_id(player):
    return re.findall("[a-z]{2}_[0-9]+", str(player))[0]


def read_player_name(player):
    return player.text.strip()


def read_info_from_onmouseover(player_soup, player_object):
    onmouseover_soup = get_player_onmouseover(player_soup)
    read_player_basic_info(onmouseover_soup, player_object)
    read_parameters_and_disposable_item(onmouseover_soup, player_object)
    read_arcana(onmouseover_soup, player_object)
    read_evolutions(onmouseover_soup, player_object)


def get_player_onmouseover(player):
    onmouseover = player['onmouseover'][16:player['onmouseover'].rfind("CAPTIONFONTCLASS")-4]
    onmouseover_soup = BeautifulSoup(onmouseover, 'html.parser')
    return onmouseover_soup


def read_player_basic_info(soup, player_object):
    params = soup.find_all('div')[2].find_all('b')
    player_object.set_race(params[0].text)
    player_object.set_level(params[2].text)
    player_object.set_parameter("defense", params[3].text)
    player_object.set_parameter("hp", params[4].text.split()[0])
    player_object.set_parameter("blood_points", params[5].text.split()[0])
    player_object.set_parameter("luck", params[6].text)
    player_object.set_parameter("initiative", params[7].text)


def read_parameters_and_disposable_item(soup, player_object):
    parameters_spans = soup.find_all('span')
    parameters = [param.text for param in parameters_spans[1:10]]
    parameters_names = ['strength', 'agility', 'toughness', 'appearance', 'charisma', 'reputation',
                        'perception', 'intelligence', 'knowledge']
    for i in range(len(parameters)):
        player_object.set_parameter(parameters_names[i], parameters[i])
    if len(parameters_spans) >= 11:
        player_object.set_disposable_item(parameters_spans[10].text if parameters_spans[10].has_attr("class") else None)


def basic_read(soup, tag_filter, text_start, text_end=None):
    div = soup.find('div')
    reading = div.find(tag_filter)
    if text_end:
        return reading.text[text_start:text_end].split(", ") if reading else []
    else:
        return reading.text[text_start:].split(", ") if reading else []


def read_arcana(soup, player_object):
    arcana = basic_read(soup, arcana_div, 16, -1)
    player_object.set_arcana(list_to_dictionary(arcana))


def arcana_div(tag):
    return tag.name == 'div' and 'arkana' in tag.get_text()


def read_evolutions(soup, player_object):
    evolutions = basic_read(soup, evolutions_div, 18, -1)
    player_object.set_evolutions(list_to_dictionary(evolutions))


def evolutions_div(tag):
    return tag.name == 'div' and 'ewolucje' in tag.get_text()


