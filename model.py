from functions import translate_parameter


class Report:

    def __init__(self, url, report_type):
        self.url = url
        self.report_type = report_type
        self.attacker = None
        self.defender = None
        self.winner = None
        self.language = 'en'

    def __str__(self):
        return self.report_type + ": " + self.attacker + " vs " + self.defender

    def set_language(self, language):
        self.language = language

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
        self.leader = True if "(@)" in name else False
        self.initiator = True if "(*)" in name else False
        self.clan = clan
        self.race = None
        self.level = None
        self.parameters = {}
        self.disposable_item = None
        self.arcana = {}
        self.evolutions = {}
        self.talismans = {}
        self.tactic = None
        self.time_bonuses = {}
        self.actions_counters = {"attacks": 0, "hits": 0, "misses": 0, "crits": 0,
                                 "defences": 0, "successful_defs": 0, "dodges": 0, "crit_taken": 0,
                                 "heals": 0, "hp_recovered": 0}
        self.comments = []
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

    @classmethod
    def get_top_players(cls, parameter, ascending=True, limit=5, language='en'):
        top_list = sorted(cls.players_list, key=lambda x: x.parameters[parameter], reverse=ascending)[:limit]
        return [{'Klan': x.clan, 'Gracz': x.name,
                 translate_parameter(parameter, language).capitalize(): x.parameters[parameter]}
                for x in top_list]

    def set_race(self, race):
        self.race = race

    def set_level(self, level):
        self.level = int(level)

    def set_parameter(self, parameter, value):
        self.parameters.update({parameter: int(value)})

    def set_parameters(self, parameters):
        for key, value in parameters.items():
            self.parameters.update({key: int(value)})

    def set_disposable_item(self, item):
        self.disposable_item = item

    def set_arcana(self, arcana):
        self.arcana.update(arcana)

    def set_evolutions(self, evolutions):
        self.evolutions.update(evolutions)

    def set_talismans(self, talismans):
        self.talismans.update(talismans)

    def set_tactic(self, tactic):
        self.tactic = tactic

    def set_time_bonuses(self, time_bonuses):
        self.time_bonuses.update(time_bonuses)

### actions ###
    def update_attacks(self):
        self.actions_counters["attacks"] = self.actions_counters.get("attacks") + 1

    def update_hits(self):
        self.update_attacks()
        self.actions_counters["hits"] = self.actions_counters.get("hits") + 1

    def update_misses(self):
        self.update_attacks()
        self.actions_counters["misses"] = self.actions_counters.get("misses") + 1

    def update_crits(self):
        self.update_hits()
        self.actions_counters["crits"] = self.actions_counters.get("crits") + 1

    def update_defences(self):
        self.actions_counters["defences"] = self.actions_counters.get("defences") + 1

    def update_successful_defences(self):
        self.update_defences()
        self.actions_counters["successful_defs"] = self.actions_counters.get("successful_defs") + 1

    def update_dodges(self):
        self.update_defences()
        self.actions_counters["dodges"] = self.actions_counters.get("dodges") + 1

    def update_crit_defs(self):
        self.update_defences()
        self.actions_counters["crit_taken"] = self.actions_counters.get("crit_taken") + 1

    def update_heals(self, hp):
        self.actions_counters["heals"] = self.actions_counters.get("heals") + 1
        self.actions_counters["hp_recovered"] = self.actions_counters.get("hp_recovered") + hp

### actions end ###

    def add_comment(self, comment):
        self.comments.append(comment)

    def check_ninja(self):
        if "Ninja" in self.time_bonuses:
            if self.time_bonuses["Ninja"] != 5:
                self.add_comment(f"Niski poziom Ninja ({self.time_bonuses['Ninja']})")
        else:
            self.add_comment("Brak Ninja")

    def check_arcanas(self):
        wrong_arcana = []
        if "Maska Kaliguli" in self.arcana and "Maska strachu" not in self.talismans:
            if self.arcana["Maska Kaliguli"] != 1:
                wrong_arcana.append("Maska Strachu")
        if "Maska Adonisa" in self.arcana and "Maska władzy" not in self.talismans:
            if self.arcana["Maska Adonisa"] != 1:
                wrong_arcana.append("Maska Adonisa")
        if "Skóra Bestii" in self.arcana and "Aura bestii" not in self.talismans:
            if self.arcana["Skóra Bestii"] != 1:
                wrong_arcana.append("Skóra Bestii")
        if wrong_arcana:
            self.add_comment("Arkana bez talizmanu: " + ", ".join(wrong_arcana))

    def check_talismans(self):
        wrong_talismans = []
        if "Kamień zła" in self.talismans:
            wrong_talismans.append("Kamień zła")
        if "Kamień dobra" in self.talismans:
            wrong_talismans.append("Kamień dobra")
        if wrong_talismans:
            self.add_comment("Zbędne talizmany: " + ", ".join(wrong_talismans))
        wrong_talismans = []
        if "Maska strachu" in self.talismans and "Maska Kaliguli" not in self.arcana:
            wrong_talismans.append("Maska strachu")
        if "Maska władzy" in self.talismans and "Maska Adonisa" not in self.arcana:
            wrong_talismans.append("Maska władzy")
        if "Szpony mocy" in self.talismans and "Nocny Łowca" not in self.arcana:
            wrong_talismans.append("Szpony mocy")
        if "Życie i śmierć" in self.talismans and "Tchnienie Śmierci" not in self.arcana:
            wrong_talismans.append("Życie i śmierć")
        if "Otchłań ciszy" in self.talismans and "Cisza Krwi" not in self.arcana:
            wrong_talismans.append("Otchłań ciszy")
        if "Potęga mocy" in self.talismans and "Wyssanie Mocy" not in self.arcana:
            wrong_talismans.append("Potęga mocy")
        if "Furia bestii" in self.talismans and "Dziki Szał" not in self.arcana:
            wrong_talismans.append("Furia bestii")
        if "Aura bestii" in self.talismans and "Skóra Bestii" not in self.arcana:
            wrong_talismans.append("Aura bestii")
        if "Pieśń krwi" in self.talismans and "Krew Życia" not in self.arcana:
            wrong_talismans.append("Pieśń krwii")
        if wrong_talismans:
            self.add_comment("Talizmany bez arkan: " + ", ".join(wrong_talismans))

    def get_comments(self):
        return '; '.join(self.comments) if self.comments else "Brak uwag"



