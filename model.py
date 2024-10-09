class Report:

    def __init__(self, url, report_type):
        self.url = url
        self.report_type = report_type
        self.attacker = None
        self.defender = None

    def __str__(self):
        return self.report_type + ": " + self.attacker + " vs " + self.defender

    def set_attacker(self, attacker):
        self.attacker = attacker

    def set_defender(self, defender):
        self.defender = defender


class Player:

    name: str
    players_list = []

    def __init__(self, player_id, name, clan):
        self.id = player_id
        self.name = name.replace("(@)", "").replace("(*)", "").strip()
        self.clan = clan
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
