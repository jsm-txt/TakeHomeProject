import jinja2
import os
import requests
from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file


app = Flask(__name__)

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



if __name__ == '__main__':
    app.run(debug=True)
