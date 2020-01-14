"""
Note this file contains _NO_ flask functionality.
Instead it makes a file that takes the input dictionary Flask gives us,
and returns the desired result.

This allows us to test if our modeling is working, without having to worry
about whether Flask is working. A short check is run at the bottom of the file.
"""

import pickle
import numpy as np
import pandas as pd

# Open relevant models
with open("static/models/elas_sel.pkl", "rb") as f:
    elas_sel = pickle.load(f)
with open("static/models/scaler_sel_p05.pkl","rb") as g:
    scaler = pickle.load(g)
with open("static/models/sim_scaler.pkl","rb") as g:
    sim_scaler = pickle.load(g)
with open("static/models/neigh.pkl","rb") as g:
    neigh = pickle.load(g)
with open("static/data/lax_price_change_df.pickle","rb") as g:
    price_change_df = pickle.load(g)
with open("static/data/lax_X_flask.pickle","rb") as g:
    X_flask = pickle.load(g)


feature_names = elas_sel.feature_names
feature_display_names = elas_sel.feature_display_names
# all of the attributes of the model are also saved in the pickle file
# like feature_names and target_names, which are all stored as key value pairs

def num_extract(inputs,start,end):
    """
    Input:
    feature_dict: a dictionary of the form {"feature_name": "value"}

    Output:
    Returns list with the values corresponding to the start and end indices
    """
    out = [float(inputs.get(name, 0)) for name in elas_sel.feature_names[start:end]]
    return out

def convert(string,start,end):
    """
    Input: string for selected field, start/end index in feature column set

    Output: list of values corresponding to X_test[start:end]
    """
    vars = np.zeros(end-start)
    if string == "Other":
        return vars
    elif string in feature_names[start:end]:
        vars[list(feature_names[start:end]).index(string)] = 1
        return list(vars)

def make_prediction(x_input,num_to_cat):
    """
    Input:
    feature_dict: a dictionary of the form {"feature_name": "value"}

    Function makes sure the features are fed to the model in the same order the
    model expects them.
    num_to_cat is the index where numerical vars end (those that need to be scaled)

    Output:
    Returns (x_inputs, probs) where
      x_inputs: a list of feature values in the order they appear in the model
      probs: a list of dictionaries with keys 'name', 'prob'
    """

    x_input_num = x_input[0:num_to_cat]
    x_input_cat = x_input[num_to_cat:]
    x_input_num_scaled = scaler.transform(np.array(x_input_num).reshape(1, -1)).tolist()[0]
    x_input_scaled = x_input_num_scaled + x_input_cat

    pred_price = round(np.exp(elas_sel.predict(np.array(x_input_scaled).reshape(1, -1))[0]),2)
    return pred_price

def price_boosters(date_string, price):
    """
    Calculate price boosters for time of year, day of week, and holidays
    """
    print('price')
    print(price)
    date = pd.to_datetime(date_string)
    if date > price_change_df.ds.max():
        date_string = date_string[0:-4] + '2020'
        date = pd.to_datetime(date_string)
    if date < price_change_df.ds.min():
        date_string = date_string[1:-4] + '2019'
        date = pd.to_datetime(date_string)
    boosters = price_change_df[price_change_df.ds == date][[
        'weekly_percentage', 'holiday_percentage', 'yearly_percentage'
    ]].values[0]
    weekly = round(boosters[0] * price, 2)
    holiday = round(boosters[1] * price, 2)
    seasonal = round(boosters[2] * price, 2)
    total = round(price + weekly + holiday + seasonal,2)
    return weekly, holiday, seasonal, total

# def similar_listings(accom, baths, neigh, room):
#     """
#     Find 3 similar listings to one described in the function call
#     """
#     room = room[5:]
#     neigh=neigh[6:]
#     sim = X_flask[(X_flask.accommodates == accom) & (X_flask.bathrooms == baths) &
#                  (X_flask.neighbourhood_compressed == neigh) &
#                  (X_flask.room_type == room)][[
#                      'name', 'picture_url', 'neighbourhood', 'property_type',
#                      'bathrooms', 'bedrooms', 'beds', 'price', 'listing_url'
#                  ]]
#     prices = sim.price.str.replace('$','').str.replace(',','').apply(lambda s: float(s))
#     max_min_index = [prices.idxmin(),prices.idxmax()]
#     sim = sim.loc[max_min_index]
#     name = list(sim.name)
#     print(name)
#     neighbourhood = list(sim.neighbourhood)
#     property_type=list(sim.property_type)
#     bathrooms = list(sim.bathrooms)
#     bedrooms = list(sim.bedrooms)
#     beds = list(sim.beds)
#     price=list(sim.price)
#     listing_url=list(sim.listing_url)
#     picture_url=list(sim.picture_url)
#
#     return name, neighbourhood, property_type, bathrooms, bedrooms, beds, price, listing_url, picture_url
def similar_listings2(sim_input):
    sim_input_scaled = sim_scaler.transform(np.array(sim_input).reshape(1, -1))
    kneighbors = list(neigh.kneighbors([sim_input_scaled[0]])[1][0])
    print(kneighbors)
    sim = X_flask.iloc[kneighbors][[
                     'name', 'picture_url', 'neighbourhood', 'property_type',
                     'bathrooms', 'bedrooms', 'beds', 'price', 'listing_url','room_type'
                 ]]
    name = list(sim.name)
    print(name)
    neighbourhood = list(sim.neighbourhood)
    property_type=list(sim.property_type)
    room_type = list(sim.room_type)
    bathrooms = list(sim.bathrooms.astype(int))
    bedrooms = list(sim.bedrooms.astype(int))
    beds = list(sim.beds.astype(int))
    price=list(sim.price)
    listing_url=list(sim.listing_url)
    picture_url=list(sim.picture_url)

    return name, neighbourhood, property_type,room_type, bathrooms, bedrooms, beds, price, listing_url, picture_url


# This section checks that the prediction code runs properly
# To run, type "python predictor_api.py" in the terminal.
#
# The if __name__='__main__' section ensures this code only runs
# when running this file; it doesn't run when importing
if __name__ == '__main__':
    from pprint import pprint
    print("Checking to see what setting all params to 0 predicts")
    features = {f: '0' for f in feature_names}
    print('Features are')
    pprint(features)

    x_input, probs = make_prediction(features)
    print(f'Input values: {x_input}')
    print('Output probabilities')
    pprint(probs)
