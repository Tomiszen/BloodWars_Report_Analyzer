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



