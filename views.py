import streamlit as st


def check_icon(result):
    return ":crown:" if result else ":skull:"


def display_clans(player, report):
    col1, col2 = st.columns(2)
    col1.write(":red[Atakujący:]")
    attackers = player.get_clan_players(report.attacker)
    col1.subheader(report.attacker + check_icon(report.check_attacker_won()) + "(" + str(len(attackers)) + ")", divider="orange")
    with col1.expander(":red[Lista graczy:]"):
        players = "".join(["- " + vampire.name + "\n" for vampire in attackers])
        st.markdown(players)
    col2.write(":blue[Obrońca:]")
    defenders = player.get_clan_players(report.defender)
    col2.subheader(report.defender + check_icon(report.check_defender_won()) + "(" + str(len(defenders)) + ")", divider="orange")
    with col2.expander(":blue[Lista graczy:]"):
        players = "".join(["- " + vampire.name + "\n" for vampire in defenders])
        st.markdown(players)