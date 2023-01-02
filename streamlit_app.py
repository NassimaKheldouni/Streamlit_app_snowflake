
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


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
st.header("Fruityvice Fruit Advice!")

#create the function to get fruityvice data 
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
  

try:
   fruit_choice = st.text_input('What fruit would you like information about?')
   if not fruit_choice: 
      st.error("Please select a fruit to get information")
   
   else:
      st.dataframe(get_fruityvice_data(fruit_choice))
   
except URLError as e: 
   st.error()


st.header("The fruit_load_list contains:")

#Snowflake related functions

def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * FROM fruit_load_list")
      return my_cur.fetchall()
#Add button to load the fruit list 
if st.button("Get fruit_load_list"):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   st.dataframe(my_data_rows)
   

#STOP
#st.stop()

#Allow the end user to add fruit to the list 
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('from streamlit')")
      return "Thanks for adding" + new_fruit
   
add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   st.text(insert_row_snowflake(add_my_fruit))
   
   
   
