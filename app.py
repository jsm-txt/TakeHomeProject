import jinja2
import os
import requests
from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Blueprint, Flask, render_template, request

from flask_pymongo import PyMongo


app = Flask(__name__)

class Config(object):
    DEBUG = True
    MONGO_URI = os.getenv("MONGO_URI")

app.config.from_object(Config)
mongo = PyMongo(app)
db = mongo.db
main = Blueprint("main", __name__)
app.register_blueprint(main)


load_dotenv()
API_KEY = os.getenv('API_KEY')

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('data'),
])
app.jinja_loader = my_loader

pp = PrettyPrinter(indent=4)


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():

    context = {
        
    }
    return render_template('home.html', **context)

def get_units(units):
    return 'F' if units == 'imperial' else 'C' 

@app.route('/results')
def results():
    city = request.args.get('city')
    units = request.args.get('units')

    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
  
        'appid': API_KEY,

        'units': 'imperial'
    }

    result_json = requests.get(url, params=params).json()

    pp.pprint(result_json)

    context = {
        'date': datetime.now(),
        'city': city,
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': result_json['sys']['sunrise'],
        'sunset': result_json['sys']['sunset'],
        'units_letter': get_units(units)
    }

    return render_template('results.html', **context)

@app.route('/reaction')
def reaction():
    reaction = request.args.get('reaction')

    context = {
        'reaction': reaction
    }

    return render_template('reaction.html',**context)

if __name__ == '__main__':
    app.run(debug=True)
