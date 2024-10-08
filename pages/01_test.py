import streamlit as st
import time

st.warning("warning")
st.success("success")
st.error("error")
st.info("info")
st.code('''st.text("text", help="pomoc")''')

col1, col2 = st.columns(2)
col1.multiselect("Litera", ["a", "b", "c"], ["a", "c"])
col2.selectbox("Cyfra", ("1", "2", "3"))

link = st.text_input(label=":link do raportu: link")

st.write(link)

btn = st.button("Zapisz", type="primary")
btn2 = st.button("Odczyt", type="secondary")
if btn:
    with st.spinner("Zapisuję"):
        time.sleep(5)

    st.balloons()
    time.sleep(4)
    st.rerun()