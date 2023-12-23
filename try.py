import streamlit as st
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table for storing user information
c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT
             )''')

# Function for user registration
def user_registration():
    st.subheader("Create a New Account")
    
    # Create a form to capture user input
    with st.form(key='registration_form'):
        new_username = st.text_input("Enter a new username")
        new_password = st.text_input("Enter a new password", type="password")
        submit_button = st.form_submit_button(label='Create Account')
    
        # Check if form has been submitted
        if submit_button:
            # Check if username already exists in the database
            result = c.execute("SELECT * FROM users WHERE username=?", (new_username,))
            existing_user = result.fetchone()
            if existing_user:
                st.warning("This username already exists. Please try a different username.")
            else:
                # Add the new user to the database
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
                conn.commit()
                st.success("Your account has been created!")
                st.info("Please log in to your new account.")
                st.stop()

# Function for user login
def user_login():
    st.subheader("Login to Your Account")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='login')
        if submit_button:
        # Check if the entered username and password match any existing user in the database
            result = c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = result.fetchone()
            if user:
                st.success("You have successfully logged in!")
                st.balloons()
            else:
                st.error("Invalid username or password. Please try again.")

# Streamlit app
def app():
    st.set_page_config(page_title="Login and Sign Up Example", page_icon=":guardsman:", layout="wide")
    st.title("Login and Sign Up Example")
    
    # Sidebar menu
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Select an option", menu)
    
    # Show appropriate page based on user's choice
    if choice == "Sign Up":
        user_registration()
    elif choice == "Login":
        user_login()

if __name__ == '__main__':
    app()
