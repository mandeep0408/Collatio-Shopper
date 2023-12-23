import streamlit as st
import main
import streamlit as st
import time
from flipkart import flipkart_search_product
from snapdeal import snapdeal_search_product
from main import  show_project2
import pandas as pd
import os
import glob
import base64
from PIL import Image
import requests
from io import BytesIO
import sqlite3

st.set_page_config(
    # page_title="Collatio Shopper",
    page_icon=":sunglasses:",
    layout="wide",
    initial_sidebar_state="expanded",
    #background_color="#f5f5f5",
    )
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

# Define functions for Project 1 and Project 2
def show_project1():
    #background image
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    add_bg_from_local('3.png')

    #deleting all the csv
    from delete import delete_csv_files
    folder_path = 'C:\\Users\\NIKITA\\Desktop\\COLLATIO SHOPPER\\testing\\testing'
    delete_csv_files(folder_path)

    st.title("Collatio Shopper")
    # create a search bar using streamlit
    with st.form(key='product_search'):
        search_term = st.text_input('Search for a product on Flipkart/Snapdeal')
        gender = st.text_input('Enter your gender')
        
        # add platform selection options
        platforms = st.multiselect('Select platform(s)', ['Flipkart', 'Snapdeal'])
        
        # add a search button
        submitted = st.form_submit_button(label='Search')

        col1, col2 = st.columns(2)
        

    if submitted:
        st.write("Here are your favorite products from favorite websites")
        st.write('Top 5 products with the least price currently listed:')

        if search_term and platforms:
            for platform in platforms:

                if platform == 'Flipkart':
                    flipkart_search_product(search_term, gender)

                    df = pd.read_csv(search_term + "_" + gender + "_" + "flipkart.csv")

                    # Sort the DataFrame by current price in ascending order
                    df = df.sort_values('currentprice', ascending=True)

                    # Create a Streamlit web app
                    col1, col2 = st.columns(2)
                    col1.title('Flipkart')

                    # Display the top 5 products with the least price
                    for i in range(5):
                        response = requests.get(df.iloc[i]['imageurl'])
                        img = Image.open(BytesIO(response.content))
                        img = img.resize((224, 224))  # Resize the image to desired size
                        col1.image(img, width=224)
                        col1.write(
                            f"<p style='background-color: black; color: white; padding: 5px;'>Product Name: {df.iloc[i]['productName']}</p>",
                            unsafe_allow_html=True)
                        col1.write(f"Discounted Price: Rs.{df.iloc[i]['currentprice']}")
                        col1.write(f"Original Price: Rs.{df.iloc[i]['mrp']}")

                elif platform == 'Snapdeal':
                    snapdeal_search_product(search_term, gender)
                    df = pd.read_csv(search_term + "_" + gender + "_" + "snapdeal.csv")

                    # Sort the DataFrame by current price in ascending order
                    df = df.sort_values('Discounted Price', ascending=True)

                    # Create a Streamlit web app
                    col2.title('Snapdeal')

                    # Display the top 5 products with the least price
                    num_products_displayed = 0  # Counter to keep track of number of products displayed
                    for i in range(len(df)):
                        if num_products_displayed == 5:
                            break  # Break the loop once 5 products are displayed

                        if pd.isna(df.iloc[i]['Image Url']):
                            continue  # Skip the product if image URL is not available

                        response = requests.get(df.iloc[i]['Image Url'])
                        img = Image.open(BytesIO(response.content))
                        img = img.resize((224, 224))  # Resize the image to desired size
                        col2.image(img, width=224)
                        col2.write(
                            f"<p style='background-color: black; color: white; padding: 5px;'>Product Name: {df.iloc[i]['Product Name']}</p>",
                            unsafe_allow_html=True)
                        col2.write(f"Discounted Price: Rs.{df.iloc[i]['Discounted Price']}")
                        col2.write(f"Original Price: Rs.{df.iloc[i]['Original Price']}")

                        num_products_displayed += 1
            st.success('Click on Search for Different Products')
        else:
            st.warning('Please enter a search term and select at least one platform.')

# Define the app
def app():

    # Add a sidebar menu with options to run each project
    menu = ["Login", "Sign Up", "Project 1", "Project 2"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Show appropriate page based on user's choice
    if choice == "Login":
        # Call the login function
        user_login()
    elif choice == "Sign Up":
        # Call the sign up function
        user_registration()
    elif choice == "Project 1":
        # Call the project1 function
        show_project1()
    elif choice == "Project 2":
        # Call the project2 function
        main.show_project2()

# Call the app
if __name__ == "__main__":
    app()
