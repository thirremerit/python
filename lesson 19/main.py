import pandas as pd
import streamlit as st
import plotly.express as px

books_df= pd.read_csv("data.csv")


# Streamlit app title

st.title("Bestselling books")
st.write("This app analyzes the amazon yop drllinh books")

st.sidebar.header("Add new book Data")

with st.sidebar.form("book_form"):
    new_name= st.text_input("Book name")
    new_author = st.text_input("Author")
    new_user_rating = st.slider("User Rating",0.0,5.0,0.0,0.1)
    new_reviews = st.number_input("Reviews",min_value=0,step=1)
    new_price= st.number_input("Price",min_value=0,step=1)
    new_year = st.number_input("Year", min_value=2009, step=1)
    new_genre = st.selectbox("Genre",books_df['Genre'].unique())
    submit_button=st.form_submit_button(label="Add Book")

if submit_button:
    new_data={
        'Name':new_name,
        'Author':new_author,
        'User Rating':new_user_rating,
        'Raviews':new_reviews,
        'Price':new_price,
        "Year":new_year,
        'Genre':new_genre
    }

    books_df = pd.concat([pd.DataFrame(new_data,index=[0]),books_df],ignore_index=True)
    books_df.to_csv("dat.csv",index=False)
