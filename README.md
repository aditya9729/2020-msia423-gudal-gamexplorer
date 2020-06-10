# The GamExplorer - A Video Game Recommender

Created by - Aditya Gudal 

QA - Aditya Tyagi 

- [Project Charter](#project-charter)
- [Sprint Plan](#sprint-plan)
- [Backlog](#backlog)
- [Icebox](#icebox)
	
## Project Charter

### Vision
This project is an attempt to recommend video games across different platforms to a community of gamers. The idea is to speed up the 
decision to buy games and increase customer satisfaction by provide interesting recommendations. Also, it is a great way to bring the inner gamer out during quarantine.

### Mission
This application will prompt users to fill in their favorite game that they like .The model will then recommend 10 games based on models from item based collaborative filtering, hybrid collaborative filtering techniques and clustering techniques.Furthermore. Based on the user's favorite game and the recommendations, a gamer profile will be made(after collecting their data separately). The idea is to surprise the user as much as possible and provide a great experience.

#### Data sources:
   * RAWG Database:One of the largest video game databases, API : https://rawg.io/apidocs 
 
### Success Criteria
#### Machine Learning metrics constituiting success:
 * For recommender techniques (Alternating Least Squares), we would like to compute a Root Mean Square Error and Mean Absolute Error of less than 0.4. 
 * For K-means clustering, we would like first determine number of clusters based on Pseudo F1 score, Silhoutte metric and reduction of SSE(SSE below 0.6).
 
#### Business metrics 
constituiting success:
 * If the number of users who downloaded the application are greater than 100,000 
 * If the number of users who use the application are greater than 20,000.
 * If 60% of the users return to the application(implicit success).
 * If more than 3000 of the users provide a rating to the application that is positive(explicit success).
 * If the time spent on the website in one session is atleast 5 minutes.

## Sprint Plan

### Initiative 1: Data validation, Collection and Cleaning.
* Epic 1: Collecting data from various resources.(Week 1)- Done
  * Story 1: Identify and Shortlist relevant data.(Week 1) - Done
  * Story 2: Understand the data dictionary from the resources.(Week 1)-Done
 * Epic 2: Data integration and cleaning.(Week 1 and 2) - Done
   * Story 1: Create a clean datasets - rawgapi using raw data.(Week 1)-Done
   * Story 2: Remove data errors, duplicated missing values and transform data.(Week 2)-Done
  
### Initiative 2: Preliminary analysis, exploration and model building.
* Epic 1: Exploratory Data Analysis.(Week 3,4) - Done
  * Story 1: Identify top publishers, games with high score and rating.(Week 3,4) - Done
  * Story 2: Identify which genre is the most popular and look at overall sales and continent wise sales. (Week 3,4)- Done
* Epic 2: Feature Engineering and Selection.(Week 3,4)-Done
* Epic 3: Clustering of numerical data.(Week 7)-Done - Didn't use this approach
  * Story 1: Scale the features and transform if required.(Week 7)-Done
  * Story 2: Identify clustering technique: K-means, Hierarchial Clustering, GMMs or Mean Isoshift methods.(Week 7)-Done
  * Story 3: Develop and profile clusters and understand item profiles.(Week 7)-ICEBOX
* Epic 4: Recommender System building.(Week 7,8)-Done
  * Story 1: Identifying which algorithm to use - Item-Item collaborative filtering,Alternating least squares or truncated SVDs.(Week 7,8)-Done
* Epic 5: Recommend Popular, novel games and similar users to the users preference.(Week 7,8)-ICEBOX
* Epic 6: Iterate through the model again and validate.(Week 7,8) Done

### Initiative 3: Creation of the Application.
* Epic 1: Construct SQL databases.(Week 5)-Done
   * Story 1: SQL Database storing all the data for the relevant to the application.(Week 5)- ICEBOX
   * Story 2: Construct a SQL database that will store user's favorite game and 10 recommendations.(Week 5)- Done
* Epic 2: Design and build user interface.(Week 8,9)-Done
   * Story 1: Iterate through ideas using a wireframe for the landing page.(Week 8,9)-Done
   * Story 2: Creating the landing page of application.(Week 8,9)-Done
   * Story 3: Design user interface and input layout.(Week 8,9)-Done
   * Story 4: Creating a gamer profile survey.(Week 8,9)-Done
   * Story 5: Building a gamer motivation chart.(Week 8,9)-ICEBOX
* Epic 3: Use S3 to store raw data on AWS.(Week 5)-Done
* Epic 4: Configure Flask App and develop the Flask App.(Week 9)-Done

### Initiative 4: Software testing and application development
* Epic 1: Deploy the best model after testing which works better.(Week 9)-Done
* Epic 2: Build unit and logging tests to evaluate functionality.(Week 7,8,9)-Done
* Epic 3: Design and conduct A/B tests to evaluate application versions.(Week 9)-ICEBOX
* Epic 4: Running Application in Docker.(Week 9)-Done
   * Story 1: Build Image.
   * Story 2: Run container.
* Epic 5: Finalize Application.(Week 9)-Done

## Backlog
* Initiative1->Epic1(Done)
* Initiative2->Epic1->Story1(Done)
* Initiative2->Epic1->Story2(Done)
* Initiative3->Epic3(Done)
* Initiative1->Epic2(Done)
* Initiative2->Epic1.Story3(Done)
* Initiative2->Epic2(Done)
* Initiative2->Epic3(Done
* Initiative2->Epic4(Done)
* Initiative2->Epic5(Done)
* Initiative2->Epic6(Done)
* Initiative4->Epic1,Epic2,Epic5(Done)

## Icebox
*  Initiative2->Epic3->Story3
* Initiative2->Epic5
* Initiative3->Epic1->Story1
* Initiative3->Epic2->Story4
* Initiative4->Epic3

# MSiA423 GameExplorer Repository

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the Model Pipeline](#running-the-model-pipeline)
- [Running the Flask App](#running-the-flask-App)
- [Running Unit Tests](#running-unit-tests)
- [Configurations](#configurations)
 * [Configure environment variables](#configure-environment-variables)
 * [Configure database connection string](#configure-database-connection-string)
 * [Configure S3 bucket](#configure-s3-bucket)
- [Running Model Pipeline Individual Steps](#running-model-pipeline-individual-steps)
 * [Ingest data from source and upload to S3 bucket](#ingest-data-from-source-and-upload-to-S3-bucket)
 * [Clean and featurize data](#clean-and-featurize-data)
 * [Train model](#train-model)
 * [Score model](#score-model)
- [Running MySQL Database in terminal](#running-mysql-database-in-terminal)
 * [Configure MySQL environment variables](#configure-mysql-environment-variables)
 * [Run MySQL in Docker](#run-my-sql-in-docker)

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
│   ├── config.py                     <- Configuration of file paths, decision variables,file names, flask configurations
│   ├── config.yaml	              <- Some file paths, URL endpoint, S3 bucket name,model hyperparameters, and columns used and dropped 
|
├── data                              <- Folder that contains data used or generated. Only the external/,sample/ and customers.db subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
|   ├── customers.db		      <- Local SQL database
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (joblib filetype), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data,python scripts for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── create_database.py                <- Creates the customers database schema
├── Dockerfile                        <- Docker file to build image games and run pipeline, app and tests
├── Makefile			      <- Makefile to sequentially run pipeline, app and tests
├── README.md                         <- Detailed instructions to run pipeline, app and tests
├── requirements.txt                  <- Python package dependencies 
├── run_mysql_client.sh               <- Runs interactive sql server based on host,username,password.
├── run_pipeline.py		      <- wrapper that runs pipeline with optional user commands
├── run_write_data_s3.py	      <- wrapper that fetches data from api and writes to s3 bucket
```

## Running the Model Pipeline
### Note :Please be connected to the northwestern VPN throughout if possible(for RDS instance atleast)
Creates all artifacts needed to support the web application.

Note: if the data has not already been ingested and uploaded to S3 (or saved locally), in the root of the repository, first run:

	python run_write_data_s3.py

OR

	python run_pipeline.py acquire_from_api
	
	python run_pipeline.py write_to_s3
	

### Running locally

In the root of the repository, run:

	make pipeline
	
### Running in Docker

#### Step 1: Build Docker image

	docker build -t games .

#### Step 2: Produce all model pipeline artifacts

Note you will need to set your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY credentials in the following command line argument.

	docker run -e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key> -e AWS_ACCESS_KEY_ID=<your-aws-access-key-id> --mount type=bind,source=$(pwd),target=/app/ games pipeline
	
Alternatively, you can set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY credentials in a config.env file in the config/ directory.

	docker run -env-file=config/config.env --mount type=bind,source=$(pwd),target=/app/ games pipeline

## Running the Flask App

### Running Locally

#### Step: Run the app

	python app.py
	
### Running in Docker

Step 1: Build the Docker image

	docker build -t games .
	
Step 2: Run the app 

First please put in SQLALCHEMY_DATABASE_URI as an environment variable for local database: sqlite:///data/customers.db

For RDS database use: {dialect}://{user}:{pw}@{host}:{port}/{db} fill in the details here and remove { }

	docker run -e SQLALCHEMY_DATABASE_URI -p 5000:5000 games app
	
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

For windows use http://127.0.0.1:5000/

### Notes on the Database

The database can be configured by specifying a connection string as the SQLALCHEMY_DATABASE_URI environment variable.
By default, if SQLALCHEMY_DATABASE_URI is not provided as an environment variable, then if the MYSQL_HOST is provided as an environment variable, an RDS database will be used to store the user responses (given that MYSQL_USER and MYSQL_PASSWORD, and MYSQL_PORT are also provided)
If MYSQL_HOST is not provided as an environment variable, then a local SQLite database in the /data folder is used to store the user responses 

## Running Unit Tests

### Running Locally

In the root of the repository, run:

	make tests
	
Running in Docker

Step 1: Build the Docker image (can use the same Docker image as the model pipeline if already built). If the Docker image for the model pipeline has already been built, you can skip this step.

	docker build -t games .
	
Step 2: Run the tests

	docker run games tests

### Configurations
1. Configure environment variables
Two sets of environment variables are required to run the model pipeline and the web application using an RDS database:

AWS credentials for the model pipeline, to upload / download files from S3:
AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID

MySQL credentials for the web application, to store user data in an RDS database:
MYSQL_USER
MYSQL_PASSWORD
MYSQL_HOST
MYSQL_PORT
MYSQL_DATABASE

If MySQL credentials are not exported as environment variables, the application will use the local SQLite database in the data directory

### Running locally

Ensure AWS credentials are in the ~/.aws/credentials file.

Export MySQL credentials by running the following commands (replacing brackets <> with your own credentials):

	export MYSQL_USER=<your-MySQL-user>
	export MYSQL_PASSWORD=<your-MYSQL-password>
	export MYSQL_HOST=<your-MySQL-host>
	export MYSQL_PORT=<your-MySQL-port>
	export MYSQL_DATABASE=your-MySQL-database>
	
Running in Docker

The environment variables can be exported in the docker run command via the -e VAR=val flag for each environment variable (see Running Model Pipeline in Docker).

Alternatively create a file called config.env file within the config/ path to store the environment variables, which will be exported to the Docker container when the scripts are executed:

To create the config.env file, from the root directory, run:

	vi config/config.env
	
Copy the code below into the config.env file and replace the bracketed <> fields with your credentials):

#### AWS credentials

	AWS_SECRET_ACCESS_KEY=<your-AWS-secret-access-key>
	AWS_ACCESS_KEY_ID=<your-AWS-access-key-id>

#### MySQL credentials

	MYSQL_USER=<your-MySQL-user>
	MYSQL_PASSWORD=<your-MYSQL-password>
	MYSQL_HOST=<your-MySQL-host>
	MYSQL_PORT=<your-MySQL-port>
	MYSQL_DATABASE=<your-MySQL-database-name>
	
Then, add --env-file=config/config.env after the applicable docker run statement to export the environment variables Docker.

2. Configure database connection string
Local MySQL

The default database name is customersdb . This default can be modified in the config.py script:

	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	if SQLALCHEMY_DATABASE_URI is not None:
   		 pass
	elif host is None:
    		SQLALCHEMY_DATABASE_URI = 'sqlite:///data/customers.db'(change this for local)
	else:
    	    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}{port}/{db}'.format(dialect=DB_DIALECT,
	    user=DB_USER,pw=DB_PW, host=DB_HOST, port=DB_PORT,db=DATABASE)
   
Local SQLite

To change the default local file path where the SQLite database is created, modify DATABASE_PATH variable in the config.py file. for populating change SQLALCHEMY_DATABASE_URI.
where HOME is the root of the directory. The DATBASE_PATH should be an absolute path, not a relative path.

3. Configure S3 bucket
To change the default S3 bucket for which files are uploaded and downloaded from, modify the S3_BUCKET variable in config.py. The S3 bucket specification can also be passed in as a command line argument (see Ingest data from source and upload to S3 bucket)

### Running Model Pipeline Individual Steps
All scripts should be executed by running python run.py <arg> in the root of the repository, where <arg> specifies the step in the model pipeline to execute. Details on the pipeline and arguments to pass are below.

1. Ingest data from source and upload to S3 bucket
To import data from the source URL (source here), run:

	python run_pipeline.py acquire_from_api --config=config/config.yaml
	
	python run_pipeline.py write_to_s3 --config=config/config.yaml
2. Fetch data from S3, run:
		
		python run_pipeline.py acquire_from_s3 --config=config/config.yaml
		
The data will be games_data.pkl stored in the /data/external folder

2. Clean and featurize raw data
To clean and pre-process, featurize the raw data file, run:

	python run_pipeline.py featurize --config=config/config.yaml
	
The clean data features numpy array and intermediate required data will by default be saved locally in the /data/external folder.

Optional argument flags / configurations

--input: input data file path
--output: to specify the file path to store output to.

3. Train model
To created the trained model objects, model artifacts (e.g., encoders, scalers), and results, run:

	python run_pipeline.py train --config=config/config.yaml
The trained model object, encoder, and scalers PKL files will by default be saved locally in the models/ folder.

Optional argument flags / configurations

--input: to specify the file path + name of the features npy file
--output: to specify the file path where the model artifacts are output -joblib file. Must be a folder path and not file name.

4.Score model 
To score model and store metrics run:

	python run_pipeline.py score --config=config/config.yaml

	
### Tests (Optional)
within tests you have 
	* test_model that conatins a model artifact(joblib file) to test on.
	* test_functions - helpers for testing basically all the functions from src.
	* test_datasets - data required(from data/external/), in the code a sample is used

In the test folder run:

	pytest run_tests.py
	
### Running MySQL in Command Line (Optional)
#### NOte make sure you are on the Northwestern VPN
Once the RDS table has been created, you can access the database via MySQL in the command line.

1. Configure MySQL environment variables
First, configure environment variables by either:

Exporting the variables directly in the command line by running the following commands:

	export MYSQL_USER=<your-MySQL-user>
	export MYSQL_PASSWORD=<your-MYSQL-password>
	export MYSQL_HOST=<your-MySQL-host>
	export MYSQL_PORT=<your-MySQL-port>
Creating a .mysqlconfig file via command vi .mysqlconfig in the root of the repository to store the code above:

	export MYSQL_USER=<your-MySQL-user>
	export MYSQL_PASSWORD=<your-MYSQL-password>
	export MYSQL_HOST=<your-MySQL-host>
	export MYSQL_PORT=<your-MySQL-port>
Then, run the following in command line to export the environment variables:

	echo 'source .mysqlconfig' >> ~/.bashrc

	source ~/.bashrc
2. Run MySQL in Docker
Access the RDS table via MySQL in command line by executing the following:

	sh run_mysql_client.sh
