# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render the HTML page via index.html using data stored in Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data_db = mongo.db.mars_data_db.find_one()

    # Return template (html) and data (mongo db)
    return render_template("index.html", mars=mars_data_db)


# Route that will call the scrape function, collect the new data, and store it in the mongo db
@app.route("/scrape")
def scrape():

    mars_data_db = mongo.db.mars_data_db

    # Call the scrape function from scrape_mars.py
    mars_data = scrape_mars.scrape()

    # Update mongo db using upsert = True (upsert will update if db already exists or create a db and insert the data)
    # {} means update/insert all entries
    mars_data_db.update({}, mars_data, upsert=True)

    # Return a redirect to the main page where everything will be displayed with index.html
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

