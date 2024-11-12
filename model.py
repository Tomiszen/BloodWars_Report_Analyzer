class Report:

    def __init__(self, url, report_type):
        self.url = url
        self.report_type = report_type
        self.attacker = None
        self.defender = None
        self.winner = None

    def __str__(self):
        return self.report_type + ": " + self.attacker + " vs " + self.defender

    def set_opponents(self, sides):
        self.attacker = sides['attacker'].strip()
        self.defender = sides['defender'].strip()

    def set_winner(self, winner):
        self.winner = winner.strip()

    def check_attacker_won(self):
        return True if (self.winner == self.attacker) else False

    def check_defender_won(self):
        return True if (self.winner == self.defender) else False


class Player:

    name: str
    players_list = []

    def __init__(self, player_id, name, clan):
        self.id = player_id
        self.name = name.replace("(@)", "").replace("(*)", "").strip()
        self.clan = clan
        self.race = None
        self.level = None
        self.parameters = {}
        self.disposable_item = None
        self.arcana = {}
        self.evolutions = {}
        self.talismans = {}
        type(self).players_list.append(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @classmethod
    def get_player(cls, player_id=None, name=None):
        if player_id:
            return list(filter(lambda elem: elem.id == player_id, cls.players_list))[0]
        elif name:
            return list(filter(lambda elem: elem.name == name, cls.players_list))[0]
        else:
            return None

    @classmethod
    def get_clan_players(cls, clan):
        return list(filter(lambda elem: elem.clan == clan, cls.players_list))

    @classmethod
    def get_players_names(cls):
        players_names_list = [player.name for player in cls.players_list]
        players_names_list.sort()
        return players_names_list

    def set_race(self, race):
        self.race = race

    def set_level(self, level):
        self.level = int(level)

    def set_parameter(self, parameter, value):
        self.parameters.update({parameter: int(value)})

    def set_disposable_item(self, item):
        self.disposable_item = item

    def set_arcana(self, arcana):
        self.arcana.update(arcana)

    def set_evolutions(self, evolutions):
        self.evolutions.update(evolutions)

    def set_talismans(self, talismans):
        self.talismans.update(talismans)