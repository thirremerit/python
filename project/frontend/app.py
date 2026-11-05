import requests
import streamlit as  st

Api = "http://127.0.0.1:8000"

set.set_page_config(page_title ="MY Book Library", page_icon="book", layout="wide")

st.markdown("""

    <style>
         .stApp{background:#f6f8fb;}
         .block-container { max-width:1050px; padding-top:2rem}
         h1,h2,h3 {color:#20334b}
         div.stButton > button[kind="primary"] {background:#246b9c; border-radius:9px}
         
    </style>
""",unsafe_allow_html=True)

def api(method,path,data=None):
    try:
        headers={"X-API-Key":st.session_state.keys()}if st.session_state.key else{}
        response = requests.request(method,API + path,json=data,headers=headers,timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestsException as error:
        message - error.response.text if error.response is not None else str(error)
        st.error(f"API error: {message}")
        return None

with st.sidebar:
    st.title("My Library")
    page= st.radio("Menu",["Dashboard","Books","Authors"])
    st.divider()
    st.text_input("Api key",type="password",key="key")

books = api("GET","/books")
authors = api("GET","/authors")

names= {author["id"]:author["name"] for author in authors}


if page =="Dashboard":
    st.title("Welcome to my library")
    st.write("Asimple page to organize your books and authors")
    a,b,c =st.columns(3)
    a.metric("total books",len(books))
    b.metric("Authors",len(authors))

    for book in books[-5:][::-1]:
        with st.container(border=True):
            st.write(f"**Z{book['title']}** -{names.get(books['author_id'],"unknown")}")


