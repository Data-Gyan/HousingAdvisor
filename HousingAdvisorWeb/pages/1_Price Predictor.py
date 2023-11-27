import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Predictor")
st.title('Housting Price Predictor - For Gurgaon')

with open('../pickle/df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('../pickle/pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# st.dataframe(df)

st.header("Enter your inputs")

# property_type
property_type = st.selectbox('Property Type', ['flat', 'house'])

# sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

# bedRoom
bedRoom = float(st.selectbox('Number of BedRoom', sorted(df['bedRoom'].unique().tolist())))

# bathroom
bathroom = float(st.selectbox('Number of BathRoom', sorted(df['bathroom'].unique().tolist())))

# balcony
balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))

# agePossession
agePossession = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

# built_up_area
built_up_area = float(st.number_input('Built Up Area'))

# servant room
servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))

# store room
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

# furnishing_type
furnishing_type = st.selectbox('Furnishing Types', sorted(df['furnishing_type'].unique().tolist()))

# luxury_category
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

# floor_category
floor_category = st.selectbox('Floor Types', sorted(df['floor_category'].unique().tolist()))

if st.button("Predict Price"):

    # Form dataframe
    data = [[property_type, sector, bedRoom, bathroom, balcony, agePossession, built_up_area, 
            servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'servant room', 'store room',
       'furnishing_type', 'luxury_category', 'floor_category']
    
    # create a dataframe
    test_df = pd.DataFrame(data, columns=columns)

    # Predict price
    base_price = np.expm1(pipeline.predict(test_df))[0]
    # display price
    low_price = base_price - 0.22
    high_price = base_price + 0.22
    
    st.text("""The price of the property should be between :\n Low = {0} Cr. \nHigh = {1} Cr.""".format(round(low_price, 2), round(high_price, 2)))
