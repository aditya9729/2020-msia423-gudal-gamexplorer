import pandas as pd
import joblib
from flask import render_template, request
import logging.config
from flask import Flask
from src.customer_database import Customer
from config import config
from src.app_helpers import fuzzy_matching,get_recommendations
import flask
import yaml
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__, template_folder='app/templates')

# Configure flask app from flask_config.py
app.config.from_pyfile('config/config.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

#initialize database
db = SQLAlchemy(app)

@app.route('/add', methods=['POST'])
def add_entry(games_list):
    """View that process a POST with new game input
    :param games_list `list`: list of recommended game names
    :param Local bool: If you want to save to a local database, let Local=True else save to RDS
    :return: persists into app
    """

    try:
        #save to database
        game_names= games_list[1]
        customer= Customer(favorite_game=request.form['game_name'], reco_game1=game_names[0],reco_game2=game_names[1],
                           reco_game3=game_names[2],reco_game4=game_names[3],reco_game5=game_names[4],reco_game6=game_names[5],
                           reco_game7=game_names[6],reco_game8=game_names[7],reco_game9=game_names[8],reco_game10=game_names[9])

        db.session.add(customer)
        db.session.commit()

        logger.info("New customer recommendation added, with fav game: %s", request.form['game_name'])

    except Exception as e:
        logger.warning("Not able to display recommendations, error page returned")



# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    """Runs the App and renders the positive or index template"""

    if request.method == 'GET':
        return (render_template('index.html'))

    if flask.request.method == 'POST':
        game_name = request.form['game_name']
        game_name=game_name.title()
        #take user input and try matching
        if not fuzzy_matching(hashmap_games,game_name):
            return (render_template('error.html', name=game_name))
        else:
            # generate recommendations
            games_list = get_recommendations(game_name,data=data,model=model,hashmap=hashmap_games)
            posters = games_list[0]
            games = games_list[1]
            released = games_list[2]
            rating=games_list[3]
            genres = games_list[4]
            platforms = games_list[5]
            stores=games_list[6]

        try:
            # add entry to database
            if fuzzy_matching(hashmap_games, game_name):
                add_entry(games_list)

                logger.info("Added entry to database")



        except Exception as e:

            logger.warning("Sorry couldn't add entry to database")


    return render_template('positive.html', posters=posters,games=games,released=released,rating=rating,
                                 genres=genres,platforms=platforms,game1stores=stores[0],game2stores=stores[1],game3stores=stores[2],
                                game4stores=stores[3],game5stores=stores[4],game6stores=stores[5],game7stores=stores[6],
                                game8stores=stores[7],game9stores=stores[8],game10stores=stores[9],search_name=game_name)




if __name__ == '__main__':

    INTERMEDIATE_DATA_PATH = config.SAVE_INTERMEDIATE_PATH

    data = pd.read_pickle(INTERMEDIATE_DATA_PATH)

    hashmap_games = {game: i for i, game in enumerate(list(data.name))}

    MODEL_PATH=config.SAVE_MODEL_PATH
    model = joblib.load(MODEL_PATH)

    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
