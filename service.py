import model
import requests
from bs4 import BeautifulSoup


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