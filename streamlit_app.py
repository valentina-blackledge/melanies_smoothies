import streamlit as st
import requests

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
my_dataframe = cnx.query("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen.strip())
        st.text(smoothiefroot_response.json())

    my_insert_stmt = "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('" + ingredients_string + "', '" + name_on_order + "')"

    if st.button('Submit Order'):
        cnx._instance.cursor().execute(my_insert_stmt)
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
