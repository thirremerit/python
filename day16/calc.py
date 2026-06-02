import streamlit as st

def kalkulo(num1,num2,operation):
    if operation=="mbledhje":
        result = num1+num2
    if operation=="zbritje":
        result = num1+num2


    return result



st.title("Simple Calculator")

num1 = st.number_input("Enter the first number", step=1)

num2 = st.number_input("Enter the second number", step=1)

operation = st.radio("select operation",["mbledhje","zbritje","shumezim","pjestim"])

result = kalkulo(num1,num2,operation)

st.write( result)