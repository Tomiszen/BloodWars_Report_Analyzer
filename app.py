import streamlit as st
import service
import time
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import model
import plotly.express as px
import plotly.graph_objects as go


st.title("Analizator aren klanowych BloodWars")
st.subheader("Made by Tomisz")

link = st.text_input(label=":link: link do raportu")

btn = st.button("Analizuj", type="primary")
if btn:
    report = service.create_report_object(link, 'Arena klanowa')
    soup = service.make_soup(report)
    if soup:
        service.get_opponents(soup, report)
        col1, col2 = st.columns(2)
        service.get_players(soup, 'attacker', report.attacker)
        service.get_players(soup, 'defender', report.defender)
        attackers = model.Player.get_clan_players(report.attacker)
        col1.write(":red[Atakujący:]")
        col1.subheader(report.attacker + "    (" + str(len(attackers)) + ")", divider="orange")
        col1.write(attackers)
        defenders = model.Player.get_clan_players(report.defender)
        col2.write(":blue[Obrońca:]")
        col2.subheader(report.defender + "    (" + str(len(defenders)) + ")", divider="orange")
        col2.write(defenders)
    else:
        st.error("Błędny link do raportu")