# Import python packages
import streamlit as st
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json()) 
fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
#from snowflake.snowpark.context import get_active_session

import streamlit as st

name_on_order = st.text_input("name on smoothie")
st.write("The name is", name_on_order)

# Write directly to the app
st.title("Customize your smoothie")
st.write(
    """choose the fruits you want in your juice
    """
)
from snowflake.snowpark.functions import col
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "choose upto 5 options:",my_dataframe,
    max_selections=5
)
if ingredients_list:
    #st.write(ingredients_list )
    #st.text(ingredients_list )
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit+' '
        st.subheader(each_fruit+'nutiotion info')
        #st.write(ingredients_string )
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        #st.text(fruityvice_response.json()) 
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    

    #st.write(my_insert_stmt)
    time_to_instert=st.button('submit order')
    if time_to_instert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
