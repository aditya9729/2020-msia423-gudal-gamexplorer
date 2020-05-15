# GameExplorer - A Video Game Recommender

Created by - Aditya Gudal 

QA - Aditya Tyagi 

- [Project Charter](#project-charter)
- [Sprint Plan](#sprint-plan)
- [Backlog](#backlog)
- [Icebox](#icebox)
	
## Project Charter

### Vision
This project is an attempt to recommend video games across different platforms to a community of gamers. The idea is to speed up the 
decision to buy games and increase customer satisfaction by provide interesting recommendations.

### Mission
This application will prompt users to fill in their favorite game that they like .The model will then recommend 10 popular games, top 10 games based on critic ratings, top 10 games based on sales and user similar games based on item based collaborative filtering, hybrid collaborative filtering techniques and clustering techniques.Furthermore. Based on the user's favorite game and the recommendations, a gamer profile will be made. The idea is to surprise the user as much as possible and provide a great experience.

####Data sources:
   * vgsales.csv link:https://www.kaggle.com/gregorut/videogamesales
   * steam-200k.csv link:https://www.kaggle.com/tamber/steam-video-games
   * metacritic_games.csv link:https://www.kaggle.com/skateddu/metacritic-games-stats-20112019
 
### Success Criteria
#### Machine Learning metrics constituiting success:
 * For recommender techniques, we would look at user-centric metrics such as satisfaction, diversity, novelty and seredipity.A survey will be taken of the user, he/she will give scores to the recommendations out of 10. Looking for on an average atleast a score of 6+ for each metric. 
 * For game profile clustering, we would like first determine number of clusters based on Pseudo F1 score, Silhoutte metric and reduction of SSE(SSE below 0.6).Then we would determine how relevant are those cluster profiles based on the question at hand i.e. the user's interest.
#### Business metrics constituiting success:
 * If the number of users who downloaded the application are greater than 500,000 
 * If the number of users who use the application are greater than 50,000.
 * If 60% of the users return to the application(implicit success).
 * If 50% of the users provide a rating to the application that is positive(explicit success).
 * If the time spent on the website in one session is atleast 5 minutes.

## Sprint Plan

### Initiative 1: Data validation, Collection and Cleaning.
* Epic 1: Collecting data from various resources.(Week 1)- Done
  * Story 1: Identify and Shortlist relevant data.(Week 1) - Done
  * Story 2: Understand the data dictionary from the resources.(Week 1)-Done
 * Epic 2: Data integration and cleaning.(Week 1 and 2) - Done
   * Story 1: Create a clean datasets(sales,steam,metacritic) using raw data.(Week 1)-Done
   * Story 2: Remove data errors, duplicated missing values and transform data.(Week 2)-Done
  
### Initiative 2: Preliminary analysis, exploration and model building.
* Epic 1: Exploratory Data Analysis.(Week 3,4) - Done
  * Story 1: Identify top publishers, games with high score and rating.(Week 3,4) - Done
  * Story 2: Identify which genre is the most popular and look at overall sales and continent wise sales. (Week 3,4)- Done
* Epic 2: Feature Engineering and Selection.(Week 3,4)-Done
* Epic 3: Clustering of numerical data.(Week 7)-Pending(Depends on time)
  * Story 1: Scale the features and transform if required.(Week 7)-Pending
  * Story 2: Identify clustering technique: K-means, Hierarchial Clustering, GMMs or Mean Isoshift methods.(Week 7)-Pending
  * Story 3: Develop and profile clusters and understand item profiles.(Week 7)-Pending
* Epic 4: Recommender System building.(Week 7,8)-Pending
  * Story 1: Identifying which algorithm to use - Item-Item collaborative filtering, Item based recommender or truncated SVDs.(Week 7,8)-Pending
* Epic 5: Recommend Popular, novel games and similar users to the users preference.(Week 7,8)-Pending
* Epic 6: Iterate through the model again and validate.(Week 7,8) Pending

### Initiative 3: Creation of the Application.
* Epic 1: Construct SQL databases.(Week 5)-Done
   * Story 1: SQL Database storing all the data for the relevant to the application.(Week 5)- Done
   * Story 2: Construct another SQL database that will store gamer profiles and previous recommendations to be used later.(Week 5)- Done
* Epic 2: Design and build user interface.(Week 8,9)-Pending
   * Story 1: Iterate through ideas using a wireframe for the landing page.(Week 8,9)-Pending
   * Story 2: Creating the landing page of application.(Week 8,9)-Pending
   * Story 3: Design user interface and input layout.(Week 8,9)-Pending
   * Story 4: Creating a gamer profile survey.(Week 8,9)-Pending
   * Story 5: Building a gamer motivation chart.(Week 8,9)-Pending
* Epic 3: Use S3 to store raw data on AWS.(Week 5)-Done
* Epic 4: Configure Flask App and develop the Flask App.(Week 9)-Pending

### Initiative 4: Software testing and application development
* Epic 1: Deploy the best model after testing which works better.(Week 9)-pending
* Epic 2: Build unit and logging tests to evaluate functionality.(Week 7,8,9)-Pending
* Epic 3: Design and conduct A/B tests to evaluate application versions.(Week 9)-pending
* Epic 4: Running Application in Docker.(Week 9)-pending
   * Story 1: Build Image.
   * Story 2: Run container.
* Epic 5: Finalize Application.(Week 9)-pending

## Backlog
* Initiative1->Epic1(Done)
* Initiative2->Epic1->Story1(Done)
* Initiative2->Epic1->Story2(Done)
* Initiative3->Epic1(Done)
* Initiative3->Epic3(Done)
* Initiative2->Epic4(Planned)
* Initiative2->Epic5(Planned)
* Initiative2->Epic6(Planned)
* Initiative4->Epic1,Epic2,Epic4,Epic5(Planned)

## Icebox
* Initiative1->Epic2(Progress)
* Initiative2->Epic1.Story3(Deciding)
* Initiative2->Epic2
* Initiative2->Epic3
* Initiative2->Epic5
* Initiative3->Epic2,3(Depends on Tool learnt)

# MSiA423 GameExplorer Repository

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1.Clone this repository-development](#1-clone-this-repository-development)
  * [2.Data Acquisition](#2-data-acquisition) 
  * [3.Setup environment variables](#3-setup-environment-variables)
  * [4.Set configurations](#4-set-configurations) 
  * [5.Store data to s3](#5-store-data-to-s3)
  * [6.Initialize database](#6-initialize-database)
  * [7. Configure Flask app](#7-configure-flask-app)
  * [8. Run the Flask app](#8-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── config.py                     <- Configuration of file paths, decision variables,file names.
|   ├── config.env                    <- Configuration of Secret Keys
│   ├── flaskconfig.py                <- Configurations for Flask API 
|
├── data                              <- Folder that contains data used or generated. Only the external/,sample/,clean/ subdirectories are tracked by git. 
|   ├── clean/                         <- Cleaned data files, will be synced with git
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
|  
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data,python scripts for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── create_db.py                      <- Creates the video game database schema and populates data into it.
├── Dockerfile                        <- Docker file to build image video_games and run app
├── run.py                            <- Simplifies the execution of one or more of the src scripts - stores data in s3 bucket
├── requirements.txt                  <- Python package dependencies 
├── run_mysql_client.sh               <- Runs interactive sql server based on host,username,password.
```

## Running the app
### 1.Clone this repository-development
Run the following command:

    git clone https://github.com/aditya9729/2020-msia423-gudal-gamexplorer.git
### 2.Data Acquisition
Data sources - Kaggle static files:
   * vgsales.csv link:https://www.kaggle.com/gregorut/videogamesales
   * steam-200k.csv link:https://www.kaggle.com/tamber/steam-video-games
   * metacritic_games.csv link:https://www.kaggle.com/skateddu/metacritic-games-stats-20112019
 
Steps to follow:

   * Download these files and unzip these files till you get comma separated value files.
   * Store these files within ./data/external/ (this has been done for you).
   * If you want to recreate the file storage(when there is no external and clean directory) -
    Run the following:
   
    cd ./data
    mkdir external
    mkdir clean
    cd external
   * Within external directory store the files acquired and rename them.
        * Rename 'steam-200k.csv' to 'steam.csv'.
        * Rename 'vgsales.csv' to 'sales.csv'.
        * Rename 'metacritic_games.csv' to 'metacritic.csv'.
        
### 3.Setup environment variables
Note: You will need to be on the Northwestern VPN.

Make sure you are in the root directory.

You may skip this part but this may be helpful:

Create your own virtual environment.

    conda create --name video_games_recommender
    
or use 
    
    virtualenv video_games_recommender 

Activate virtual environment.

    conda activate video_games_recommender
or use:
    
    source video_games_recommender
    
Note: If you are in a virtual or base environment run the following:

    pip install -r requirements.txt

Edit your mysql config file accordingly

    vi .mysqlconfig
or use 

    nano .mysqlconfig

* Set MYSQL_USER to the "master username" that you used to create the database server.
* Set MYSQL_PASSWORD to the "master password" that you used to create the database server.
* Set MYSQL_HOST to be the RDS instance endpoint from the console
* Set MYSQL_HOST to be 3306

Set up using the following within .mysqlconfig(please remove the caret '<' '>' signs:

    export MYSQL_USER=<YOUR_USERNAME>
    export MYSQL_PASSWORD=<YOUR_PASSWORD>
    export MYSQL_HOST=<PASTE_YOUR_HOST_HERE>
    export MYSQL_PORT=<3306>

Set the environment variables in your ~/.bashrc

    echo 'source .mysqlconfig' >> ~/.bashrc

    source ~/.bashrc
    
PLEASE NOTE: VERIFY THAT YOU ARE ON THE NORTHWESTERN VPN BEFORE YOU CONTINUE ON.        

* SET AWS_ACCESS_KEY with your aws access key.
* SET AWS_SECRET_KEY with you aws secret key.
* SET DATABASE_NAME as the database name of your rds instance.

Run the following commands and replace xxxx with keys etc.

    nano ~/.bashrc
Note you may find 'source .mysqlconfig' already, leave it untouched.

    export AWS_ACCESS_KEY=xxxx
    export AWS_SECRET_KEY=xxxxx
    source .mysqlconfig
    export DATABASE_NAME=xxxxxx
Don't forget to source:

    source ~/.bashrc
Create environments variables for docker:

    cd config
Open config.env file

    nano config.env
Set credentials - replace the xxx here too :

    AWS_SECRET_KEY=xxxxxxxxxxxxxxxxx
    AWS_ACCESS_KEY=xxxxxxxxxx


### 4.Set configurations:
Go to config.py in the config directory:

    cd config/ 
    
 Within `config.py` Please change the following bucket name your own bucket name.: 
 
    S3_BUCKET_NAME = 'nw-adityagudal-s3'
    
To create local SQLlite schema let the variable `local` be as is, currently it is:
    
    local=True
 
To create RDS instance change the variable `local`:
     
     local=False

### 5. Store data into S3

First check step 3 and 4, make sure your:
   * Environment variables are set.
   * Requirements and dependencies are met.
   * Set configurations in config.py
   
Set your bucket name in `config.py` within config directory.

Go to the root directory and Run the following:

  * Build a docker image with tag games:
  

    docker build -t games .

   * Run the docker container:
   
    docker run -it --env-file=config/config.env games run.py

    
Note this `run.py` depends on `src/store_data_in_s3.py`

This should store your data into the S3 bucket.

### 6. Initialize the database 

#### Create the database with tables
 First check step 3 and 4, make sure your:
   * Environment variables are set.
   * Requirements and dependencies are met.
   * Set configurations in config.py
 
To create the database in the location configured in `config.py` with tables customer,metacritic,sales and steam, run: 

To create a database locally use make sure to set `local=True` in `config.py`:

Go to the root directory and run:

    python create_db.py

By default, `python create_db.py ` with `local=True` creates a database at `sqlite:///data/games.db` with the tables customer, metacritic, sales and steam.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/games.db'
```

##### RDS Instance database:

Make sure you are connected to northwestern vpn

Go to step 2 and 3 and check environment variables and requirement.

 Go to the config directory and in `config.py` change local variable:
    
    local=False
 
 Go to the root directory and create the rds instance database schema by running:
       
    python create_db.py
 
 You may see a warning command here - invalid String in Game - there are games with special characters.
 PyMySQL cannot decode them but sqlite3 can.
 
 Your data is now in the database, with the schema defined, and the raw data has also been added to your S3 bucket! If you've used an RDS instance, you can verify that things have worked as expected by using the MySQL client. Run the `run_mysql_client.sh` script that allows connection to your SQL database:
 
 In the root directory run:
 
    sh run_mysql_client.sh
    
 You can query the customer, steam, metacritic and sales table in the `msia423asg5718` database as follows:
    
    use msia423asg5718;
    
Check if the 4 tables are there:
    
    show msia423asg5718;
Output is as follows:
    
    +--------------------------+
    | Tables_in_msia423asg5718 |
    +--------------------------+
    | customer                 |
    | metacritic               |
    | sales                    |
    | steam                    |
    +--------------------------+
    4 rows in set (0.04 sec)

Now run the following to check the steam table:
    
    SELECT * FROM steam LIMIT 5;
 
The output of the query is the following, do validate:

    +----+-----------+----------------------------+----------+
    | id | Userid    | Game                       | Playtime |
    +----+-----------+----------------------------+----------+
    |  1 | 151603712 | The Elder Scrolls V Skyrim |      273 |
    |  2 | 151603712 | Fallout 4                  |       87 |
    |  3 | 151603712 | Spore                      |     14.9 |
    |  4 | 151603712 | Fallout New Vegas          |     12.1 |
    |  5 | 151603712 | Left 4 Dead 2              |      8.9 |
    +----+-----------+----------------------------+----------+
    5 rows in set (0.04 sec)

Do validate this with the other tables as well!

To exit mysql:
    
    exit;
 
----------------------------------------------------------------------------------


### 5. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.

### Workaround for potential Docker problem for Windows.

It is possible that Docker will have a problem with the bash script `app/boot.sh` that is used when running on a Windows machine. Windows can encode the script wrongly so that when it copies over to the Docker image, it is corrupted. If this happens to you, try using the alternate Dockerfile, `app/Dockerfile_windows`, i.e.:

```bash
 docker build -f app/Dockerfile_windows -t pennylane .
```

then run the same `docker run` command: 

```bash
docker run -p 5000:5000 --name test pennylane
```

The new image defines the entry command as `python3 app.py` instead of `./boot.sh`. Building the sample PennyLane image this way will require initializing the database prior to building the image so that it is copied over, rather than created when the container is run. Therefore, please **do the step [Create the database with a single song](#create-the-database-with-a-single-song) above before building the image**.
