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

def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.clear()

st.set_page_config(layout="wide")
st.html(''' <style> hr { border-color: orange; } </style> ''')

st.title("Analizator aren klanowych BloodWars")
st.subheader("Made by Tomisz")

report_expander = st.expander("Raport", expanded=True if 'player' not in st.session_state else False)
link = report_expander.text_input(label=":link: link do raportu", value="https://r1.bloodwars.pl/showmsg.php?mid=202096794&key=8c479fca18")
btn = report_expander.button("Analizuj", type="primary")
st.divider()
if btn and 'player' not in st.session_state:
    clear_cache()
    Player.players_list = []
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
        service.read_battle(soup)
        for player in Player.players_list:
            service.check_player(player)
    else:
        st.error("Błędny link do raportu")

    views.display_clans(Player, report)
    st.divider()
    selected_player = st.selectbox("Gracz", Player.get_players_names())
    views.display_top_players(Player, report.language)

elif 'player' in st.session_state:
    Player = st.session_state['player']
    report = st.session_state['report']
    views.display_clans(Player, report)
    st.divider()
    selected_name = st.selectbox("Gracz", Player.get_players_names())
    views.display_player(Player.get_player(name=selected_name))
    views.display_top_players(Player, report.language)


st.sidebar.button("Refresh Program",on_click=clear_cache)


