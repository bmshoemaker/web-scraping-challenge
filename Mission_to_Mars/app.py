from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()
<<<<<<< HEAD
=======
    #mars_data = list(db.mars.find_one())
>>>>>>> 2fe01d2457abd0cc99af1c70af99539ed9efc7bd

    # Return template and data
    return render_template("index.html", mars=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_data = mongo.db.mars
    # Run the scrape function
<<<<<<< HEAD
    scraped_data = scrape_mars.mars_info()
=======
    scraped_data = scrape_mars.scrape()
>>>>>>> 2fe01d2457abd0cc99af1c70af99539ed9efc7bd

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, scraped_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
