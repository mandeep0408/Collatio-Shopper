import streamlit as st
import sqlite3

# Function for user registration
def user_registration():
    st.subheader("Create a New Account")
    new_username = st.text_input("Enter a new username")
    new_password = st.text_input("Enter a new password", type="password")
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Create a table for storing user information
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT,
                    password TEXT
                )''')
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