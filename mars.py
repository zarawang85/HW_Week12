from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
   

    mars_info = mongo.db.mars_data.find_one()
    print(bool(mars_info))
    if bool(mars_info) == False:
        mars_info = {"news_title": '',
        "news_p":'',
        "featured_image_url": '',
        "mars_weather":'',
        "mars_html_table":'',
        "hemisphere_image_urls":[{'title':'','img_url':''},{'title':'','img_url':''},{'title':'','img_url':''},{'title':'','img_url':''}]
        }
    
    # Return template and data
    return render_template("index.html", mars_info = mars_info)


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():

    # Run the scrape function
    mars = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
