import streamlit as st
import service
import time
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from model import Player
import views
import plotly.express as px
import plotly.graph_objects as go


st.title("Analizator aren klanowych BloodWars")
st.subheader("Made by Tomisz")

link = st.text_input(label=":link: link do raportu", value="https://r1.bloodwars.pl/showmsg.php?mid=202096794&key=8c479fca18")
btn = st.button("Analizuj", type="primary")
st.markdown(st.session_state)
if btn and 'player' not in st.session_state:
    report = service.create_report_object(link, 'Arena klanowa')
    soup = service.make_soup(report)
    if soup:
        report.set_opponents(service.read_opponents(soup))
        report.set_winner(service.read_winner(soup))
        service.get_players(soup, 'attacker', report.attacker)
        service.get_players(soup, 'defender', report.defender)
        attackers = Player.get_clan_players(report.attacker)
        defenders = Player.get_clan_players(report.defender)
        if 'player' not in st.session_state:
            st.session_state['player'] = Player
        if 'report' not in st.session_state:
            st.session_state['report'] = report
    else:
        st.error("Błędny link do raportu")

    views.display_clans(Player, report)
    selected_player = st.selectbox("Gracz", Player.get_players_names())

elif 'player' in st.session_state:
    Player = st.session_state['player']
    report = st.session_state['report']
    views.display_clans(Player, report)
    selected_player = st.selectbox("Gracz", Player.get_players_names())
    st.write(Player.get_player(name=selected_player).name)
    st.write(Player.get_player(name=selected_player).parameters)
    st.write(Player.get_player(name=selected_player).disposable_item)
    st.write(Player.get_player(name=selected_player).arcana)
    st.write(Player.get_player(name=selected_player).evolutions)
    st.write(Player.get_player(name=selected_player).talismans)


