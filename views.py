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


def display_player(player):
    with st.expander("Szczegóły"):
        left_col, right_col = st.columns(2)
        left_col.write(":grey[Statystyki:]")
        left_col.write(player.parameters)
        left_col.write(":grey[Jednoraz:]")
        left_col.write(player.disposable_item)
        left_col.write(":grey[Arkana:]")
        left_col.write(player.arcana)
        right_col.write(":grey[Ewolucje:]")
        right_col.write(player.evolutions)
        left_col.write(":grey[Talizmany:]")
        left_col.write(player.talismans)
        left_col.write(":grey[Taktyka indywidualna:]")
        left_col.write(player.tactic)
        right_col.write(":grey[Bonusy czasowe:]")
        right_col.write(player.time_bonuses)


def display_top_players(player, language):
    with st.form("top_players"):
        form_col1, form_col2 = st.columns(2)
        parameter = form_col1.selectbox("Parametr",
                                        ['initiative', 'strength', 'agility', 'toughness', 'appearance',
                                         'charisma', 'reputation', 'perception', 'intelligence',
                                         'knowledge', 'hp', 'defence', 'luck'])
        limit = form_col2.number_input(label="Ilu graczy", min_value=0, step=1, value=5)
        ascending = st.checkbox("Najlepsi", value=True)
        submitted = st.form_submit_button("Wyświetl")
        if submitted:
            st.table(player.get_top_players(parameter, ascending=ascending, limit=limit, language=language))