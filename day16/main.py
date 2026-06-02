import streamlit as st
from numpy.ma.core import min_val, max_val


def main():
    st.title("Hello, World!")

    st.button("click me")

st.checkbox("check")

if st.checkbox("click me to show text"):
    st.write("this text showed up cus you checked the box")


if st.button("click"):
    st.write("Button Clicked")




name = st.text_input("Enter your name:")
st.write("your name is: " , name)

age = st.number_input("Enter your age:",min_value=0,max_value=100)
st.write("your age is: " ,age)

message = st.text_area("enter a message")

if st.button("success"):
    st.success("Operations was successful")


if __name__ =="__main__":
    main()