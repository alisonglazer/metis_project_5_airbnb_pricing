# Smarter Pricing for Airbnb
## **Project 5 in the Metis Data Science Bootcamp**

Problem statement: *Can we build a smarter pricing model for Airbnb hosts to increase their revenue? Can we recommend similar successful listings?*

I focused on popular Airbnb listings in Los Angeles, CA with high occupancy rates(>65%) and deployed the project via a flask web app on [Heroku](http://airbnb-pricing.herokuapp.com/).
With tens of thousands of listings I determined which factors were most predictive of their price. Using the Inside Airbnb dataset with information on every Airbnb listing and their reviews, I considered many features including the following:

1. Bedrooms
2. Bathrooms
3. Security Deposit
4. Minimum Nights
5. Review Score
6. Availability
7. Location
8. Property Type

I used linear regression to predict the base price for a given listing. Given the importance of date in setting a nightly price, I used Facebook Prophet to forecast price fluctuations as a function of the date, considering day of week, time of year, and holidays.

To allow hosts, particularly new ones, to compare their listings to similar ones, I built a recommender system using unsupervised learning methods to compare their inputted listing to all other popular listings (those with high occupancy rates).

## Files

[`p05_Data_Clean_Feature_Setup.ipynb`](p05_Data_Clean_Feature_Setup.ipynb) shows the process to clean all of the data and prepare relevant features for modeling

[`p05_EDA_and_Regression.ipynb`](p05_EDA_and_Regression.ipynb) shows data analysis and the process of training various regression models and evaluating feature relationships and model performance

[`p05_Time_Series.ipynb`](p05_Time_Series.ipynb) shows Time Series Analysis used to forecast price fluctuations as a function of time

[`p05_Similar_Listing_Recommender.ipynb`](p05_Similar_Listing_Recommender.ipynb) uses unsupervised learning to build a recommender system to find similar successful listings

[`p05_NLP_Natural_Language_Processing.ipynb`](p05_NLP_Natural_Language_Processing.ipynb) shows analysis of Airbnb listing descriptions, using topic modeling to generate additional features for the linear regression models

[`p05_Clustering.ipynb`](p05_Clustering.ipynb) is unfinished, but uses clustering algorithms to try and create meaningful, distinct groups of Airbnb listings to improve the quality of the price suggestions

[`Web App`](web_app) files used to build the browser-based predictor tool hosted on Heroku [here](http://airbnb-pricing.herokuapp.com/)

Slides can be found [here](https://www.slideshare.net/AlisonGlazer/smarter-pricing-for-airbnb)
