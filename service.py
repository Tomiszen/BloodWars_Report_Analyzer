import model
import requests
from bs4 import BeautifulSoup
import re
from functions import list_to_dict
from model import Player


def create_report_object(url, report_type):
    return model.Report(url, "Arena klanowa")


def make_soup(report):
    r = requests.get(report.url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        html = soup.find_all("html")
        if soup.find_all("div", class_="msg-notBattleReport"):
            return False
        else:
            if html[0].has_attr('lang'):
                report.set_language(html[0]['lang'])
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


def read_info_from_onmouseover(player_soup, player):
    onmouseover_soup = get_player_onmouseover(player_soup)

    race, level, parameters = read_player_basic_info(onmouseover_soup)
    player.set_race(race)
    player.set_level(level)
    player.set_parameters(parameters)
    parameters, disposable_item = read_parameters_and_disposable_item(onmouseover_soup)
    player.set_parameters(parameters)
    player.set_disposable_item(disposable_item)
    player.set_arcana(read_arcana(onmouseover_soup))
    player.set_evolutions(read_evolutions(onmouseover_soup))
    player.set_talismans(read_talismans(onmouseover_soup))
    player.set_tactic(read_tactic(onmouseover_soup))
    player.set_time_bonuses(read_time_bonuses(onmouseover_soup))


def get_player_onmouseover(player):
    onmouseover = player['onmouseover'][16:player['onmouseover'].rfind("CAPTIONFONTCLASS")-4]
    onmouseover_soup = BeautifulSoup(onmouseover, 'html.parser')
    return onmouseover_soup


def read_player_basic_info(soup):
    params = soup.find_all('div')[2].find_all('b')
    race = params[0].text
    level = params[2].text
    parameters = {"defence": params[3].text}
    parameters.update({"hp": params[4].text.split()[0]})
    parameters.update({"blood_points": params[5].text.split()[0]})
    parameters.update({"luck": params[6].text})
    parameters.update({"initiative": params[7].text})
    return race, level, parameters


def read_parameters_and_disposable_item(soup):
    parameters_spans = soup.find_all('span')
    parameters = [param.text for param in parameters_spans[1:10]]
    parameters_names = ['strength', 'agility', 'toughness', 'appearance', 'charisma', 'reputation',
                        'perception', 'intelligence', 'knowledge']
    parameters_dict = {}
    for i in range(len(parameters)):
        parameters_dict.update({parameters_names[i]: parameters[i]})
    disposable_item = None
    if len(parameters_spans) >= 11:
        disposable_item = parameters_spans[10].text if parameters_spans[10].has_attr("class") else None
    return parameters_dict, disposable_item


def basic_read(soup, tag_filter, text_start, text_end=None):
    div = soup.find('div')
    reading = div.find(tag_filter)
    if text_end:
        return reading.text[text_start:text_end].split(", ") if reading else []
    else:
        return reading.text[text_start:].split(", ") if reading else []


def read_arcana(soup):
    arcana = basic_read(soup, arcana_div, 16, -1)
    return list_to_dict(arcana)


def arcana_div(tag):
    return tag.name == 'div' and 'arkana' in tag.get_text()


def read_evolutions(soup):
    evolutions = basic_read(soup, evolutions_div, 18, -1)
    return list_to_dict(evolutions)


def evolutions_div(tag):
    return tag.name == 'div' and 'ewolucje' in tag.get_text()


def read_talismans(soup):
    talismans = basic_read(soup, talismans_div, 11)
    return list_to_dict(talismans)


def talismans_div(tag):
    return tag.name == 'div' and 'Talizmany' in tag.get_text()


def read_tactic(soup):
    tactic = basic_read(soup, tactic_div, 22)
    return tactic[0] if tactic else None


def tactic_div(tag):
    return tag.name == 'div' and 'Taktyka' in tag.get_text()


def read_time_bonuses(soup):
    time_bonuses = basic_read(soup, time_bonuses_div, 16)
    return list_to_dict(time_bonuses, split_string=' poziom ')


def time_bonuses_div(tag):
    return tag.name == 'div' and 'czasowe' in tag.get_text()


def read_battle(soup):
    for battle_round in soup.find_all('ul', {'class': 'round'}):
        count_attacks(battle_round)
        count_heals(battle_round)

def count_attacks(battle_round):
    for message in battle_round.find_all('li', {'class': ['atkHit', 'defHit']}):
        attacker_id, defender_id = read_players_in_action(message)
        attacker = Player.get_player(player_id=attacker_id)
        defender = Player.get_player(player_id=defender_id)
        text = message.text

        if "kontratakuje" in text or "kontratak" in text:
            if "cios krytyczny" in text:
                attacker.update_cntr_crits()
                #defender.update_crit_defs()
            elif "zranion" in text:
                attacker.update_cntr_hits()
                #defender.update_defences()
            elif "wykonuje" in text:
                attacker.update_cntr_misses()
                #defender.update_dodges()
            elif "nie zostaje" in text:
                attacker.update_cntr_misses()
                #defender.update_successful_defences()


        elif "atakuje" in text:
            if "zranion" in text:
                attacker.update_hits()
                defender.update_defences()
            elif "wykonuje" in text:
                attacker.update_misses()
                defender.update_dodges()
            elif "nie zostaje" in text:
                attacker.update_misses()
                defender.update_successful_defences()
        elif "cios krytyczny" in text:
                attacker.update_crits()
                defender.update_crit_defs()

def count_heals(battle_round):
    for message in battle_round.find_all('li', {'class': 'heal'}):
        healer_id = read_players_in_action(message)
        healer = Player.get_player(player_id=healer_id)
        text = message.text
        if "odzyskuje" in text:
            hp = int(re.findall(" [0-9]+ ", str(text))[0])
            healer.update_heals(hp)


def read_players_in_action(message):
    players = re.findall("[a-z]{2}_[0-9]+", str(message))
    if len(players) == 2:
        return players[0], players[1]
    else:
        return players[0]


def add_comment(self, comment):
    self.comments.append(comment)




def check_player(player):
    player.check_ninja()
    player.check_arcanas()
    player.check_talismans()
    return None
