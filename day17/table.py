import streamlit as st

tab1,tab2,tab3 = st.tabs(["Tab 1","Tab 2","Tab 3"])

with tab1:
    st.header("Content for tab 1")
    st.write("this is the content os the first tab")
with tab2:
    st.header("Content for tab 2")
    st.write("this is the content os the first tab")
with tab3:
    st.header("Content for tab 3")
    st.write("this is the content os the first tab")
