# Making a basic calculator

import streamlit as st

# Streamlit Calculator App

st.title("Basic Calculator")
st.write("This is a simple calculator app built with Streamlit.")

num1 = st.number_input(
    label= "enter num 1 here",
    key= "num1_input"
)

num2 = st.number_input(
    label= "enter num 2 here",
    key= "num2_input"
)

if num2 == 0:
    operators = {"add", "subtract", "multiply"}
else:
    operators = {"add", "subtract", "multiply", "divide"}

operator_choice = st.selectbox( 
    label= "Choose an operator",
    options= operators,
    key= "operator_choice"
)

calculate_button = st.button(
    label= "Calculate",
    key= "calculate_button"
)

if calculate_button:
    # when the button is clicked
    if operator_choice == "add":
        result = num1 + num2
        st.write(f"The result of {num1} + {num2} is {result}")
    elif operator_choice == "subtract":
        result = num1 - num2
        st.write(f"The result of {num1} - {num2} is {result}")
    elif operator_choice == "multiply":
        result = num1 * num2
        st.write(f"The result of {num1} * {num2} is {result}")
    elif operator_choice == "divide":
        if num2 != 0:
            result = num1 / num2
            st.write(f"The result of {num1} / {num2} is {result}")
        else:
            st.write("Error: Division by zero is not allowed.")