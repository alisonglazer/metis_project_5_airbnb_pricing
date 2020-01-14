import flask
from flask import request, render_template, redirect
from ag_airbnb_api import num_extract,convert, make_prediction, price_boosters, similar_listings2, feature_names, feature_display_names,price_change_df # import from our other python file


app = flask.Flask(__name__)

@app.route("/about/",methods=["POST", "GET"])
def about():
    return render_template('about.html')

@app.route("/contact/",methods=["POST", "GET"])
def contact():
    return render_template('contact.html')


@app.route("/")
@app.route("/predict/", methods=["POST", "GET"])
def predict():
    # request.args contains all the arguments passed by our form
    # comes built in with flask. It is a dictionary of the form
    # "form name (as set in template(html))" (key): "string in the textbox" (value)
    print('request_args')
    print(request.form)
    print(request.args)
    num_vars = num_extract(request.args,0,7)
    print(type(num_vars))
    global x_input
    x_input = []
    x_input += num_vars


    # text Features
    text_vars = [0.051795, 0.094056, 0.082174, 0.046227]
    x_input += text_vars

    # amenity Features
    amen_vars = [4.684892, 2.312354]
    x_input += amen_vars

    # dummy columns below
    neigh_vars = convert(request.args.get('neigh',"neigh_Malibu"),13,27)
    x_input.extend(neigh_vars)
    room_vars = convert(request.args.get('room',"room_Entire home/apt"),27,30)
    x_input.extend(room_vars)
    prop_vars = convert(request.args.get('prop',"prop_Hotel"),30,36)
    x_input.extend(prop_vars)

    # x_input.extend([0]) ??

    global predictions
    print('x_input')
    print(x_input)
    predictions = make_prediction(x_input,13)
    # predictions = make_prediction([2.0,182.0, 182.0, 500000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0])
    # break up the tuple into those two variables
    print(predictions)

    # Get date
    date = request.args.get('date',"01/06/2019")
    weekly, holiday, seasonal, total = price_boosters(date,predictions)
    print(weekly)
    print(holiday)
    print(seasonal)
    print(total)

    return render_template('input_form.html', x_input=x_input,
                                 feature_names=feature_names,
                                 prediction=predictions,
                                 feature_display_names=feature_display_names,
                                 total=total, weekly=weekly, holiday=holiday, seasonal=seasonal,date=date)

@app.route("/answer/", methods=["POST", "GET"])
def predict2():
    print('request_args')
    print(request.form)
    print(request.args)
    num_vars = num_extract(request.args,0,7)
    print(type(num_vars))
    global x_input
    x_input = []
    x_input += num_vars


    # text Features
    text_vars = [0.051795, 0.094056, 0.082174, 0.046227]
    x_input += text_vars

    # amenity Features
    amen_vars = [4.684892, 2.312354]
    x_input += amen_vars

    # dummy columns below
    neigh = request.args.get('neigh',"neigh_Other")
    neigh_vars = convert(neigh,13,27)
    x_input.extend(neigh_vars)
    room = request.args.get('room',"room_Entire home/apt")
    room_vars = convert(room,27,30)
    x_input.extend(room_vars)
    prop_vars = convert(request.args.get('prop',"prop_Hotel"),30,36)
    x_input.extend(prop_vars)

    global predictions
    print('x_input')
    print(x_input)
    predictions = make_prediction(x_input,13)
    # predictions = make_prediction([2.0,182.0, 182.0, 500000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0])
    # break up the tuple into those two variables
    print(predictions)

    # Get date
    date = request.args.get('date',"01/06/2019")
    weekly, holiday, seasonal, total = price_boosters(date,predictions)

    # Similar listings
    accom = x_input[0]
    baths = x_input[1]
    beds = float(request.args.get('beds',"2"))
    bedrooms = float(request.args.get('bedrooms',"1"))
    sim_input=[]
    sim_input+=x_input[0:7]
    sim_input+=[4.68,2.31]
    sim_input+=x_input[13:36]
    sim_input+=[predictions]
    sim_input+=[bedrooms]
    sim_input+=[beds]
    sim_name, sim_neigh, sim_prop,sim_room, sim_baths, sim_bedrooms, sim_beds, sim_price, sim_listing_url, sim_picture_url = similar_listings2(sim_input)

    return render_template('answer.html', x_input=x_input,
                                 feature_names=feature_names,
                                 prediction=predictions,
                                 feature_display_names=feature_display_names,
                                 total=total, weekly=weekly, holiday=holiday, seasonal=seasonal,date=date,
                                 sim_name=sim_name, sim_neigh=sim_neigh, sim_prop=sim_prop, sim_room=sim_room,sim_baths=sim_baths,
                                 sim_bedrooms=sim_bedrooms, sim_beds=sim_beds, sim_price=sim_price,
                                 sim_listing_url=sim_listing_url, sim_picture_url=sim_picture_url)


if __name__=="__main__":
    # For local development:
    app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()
