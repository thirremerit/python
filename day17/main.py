
import streamlit as st


col1 ,col2 ,col3 ,col4 ,col5 = st.columns(5 ,gap="small" ,vertical_alignment="center")

with col1:
    st.header("Kolona 1")
    st.write("Content for column 1")

with col2:
    st.header("Kolona 2")
    st.write("Kolona  e 2")

with col3:
    st.header("Kolona 3")
    st.write("content for column 3")


with col4:
    st.header("Kolona 4")
    st.write("Kontent for konon 4")

with col5:
    st.header("Kolona 5")
    st.write("Kontent for konon 5")

with st.container():
    st.header("this is inside the container")
    st.write("this is inside the container")

st.write("this is outside the container")



#######side bar
st.sidebar.header("Sidebar")

st.sidebar.write("this is the sidebar")

st.sidebar.selectbox("chose an option",["Option 1","Option2","Option 3"])

st.sidebar.radio("go to",["Home","Data","Settings"])