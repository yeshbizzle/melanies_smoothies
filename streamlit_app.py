# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

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
session = get_active_session()
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
    #st.write(ingredients_string )
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    

    #st.write(my_insert_stmt)
    time_to_instert=st.button('submit order')
    if time_to_instert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
