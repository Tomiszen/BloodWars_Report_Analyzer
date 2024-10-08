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
        col1.text("Atakujący:")
        col1.subheader(report.attacker)
        col2.text("Obrońca:")
        col2.subheader(report.defender)
    else:
        st.error("Błędny link do raportu")