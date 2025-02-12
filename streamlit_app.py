# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
       """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("Smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('Search_On'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df= my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_List = st.multiselect(
    'Choose up to 5 ingredienst:'
    , my_dataframe
    , max_selections = 5
    )

if ingredients_List:
    ingredients_string = ''
    for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = """ Insert into smoothies.public.orders(ingredients, Name_on_Order)
                values ('""" + ingredients_string + """','""" +name_on_order+ """')""" 
   # st.write(my_insert_stmt)
   # st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
