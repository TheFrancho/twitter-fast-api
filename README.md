# TWITTER FAST API

Twitter Api developed on FASTApi for testing API consumption.

Includes CRUD Operations for Users and Tweets, password hashing, cascade deleting and other features on a database based on json format.

***FEATURES***

The current app allows:

- CRUD Operation for Users (Create, Read (all and individual), Update and Delete)
- CRUD  Operations for Tweets (Create, Read (all and individual), Update and Delete)
- Password hashing by Bcrypt
- Automatic ID creation by UUID4
- Register of all Tweets per Person on a new table to solve n to n dependency
- Tweets must have a valid poster
- Cascade Deletion (if a user is deleted, all its Tweets will be deleted too)
- TODO - Authentication

***PROJECT SETUP***

To run the project on your local enviroment you will be needing python 3.8.5 or older and a virtual environment of any kind.

For this example i will be using the venv module from python on a Ubuntu WSL2 environment.

- Go to your project folder
- git clone https://github.com/TheFrancho/twitter-fast-api
- python3 -m venv venv_twitter_api_project
- source venv_twitter_api_project/bin/activate
- cd twitter_api
- pip install -r requirements.txt

The project will be ready to go, now run

- uvicorn main:app --reload

Then you can go to your localhost on port 8000
- 127.0.0.1:8000/docs

![Alt text](static_files/docs_view.png?raw=true "General view")

And you will be able to play with the API if you don't want to use any API server

