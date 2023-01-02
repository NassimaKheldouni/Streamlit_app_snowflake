
import streamlit as st
import pandas as pd 

st.title("My parents healthy dinner")
st.header('Breakfast Favorites')
st.text('🥣Omega 3 & Blueberry Oatmeal')
st.text('🥗Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado toast')
   
st.header('🍉🍈🥤Build you aown fruit smoothie')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a picklist here so that they can choose the fruit they want to select
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)


#New section to display fruityvice api response 
import requests
st.header("Fruityvice Fruit Advice!")

fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# Normalize the fruityvice json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# display the response ad a dataframe
st.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit_load_list contains")
st.dataframe(my_data_rows)

add_my_fruit = st.text_input('What fruit would you like to add ?')
st.write('Thanks for adding that fruit !')
