# Ontochatbot


## Running application
In order to run the chatbot on your local maching it is necessary to have installed docker desktop.

Run the following command from the project directory:
docker compose up

The chatbot a web application that can be accessed at 
http://localhost:5000/



## Starting flask
If you want to start the application from flask directly then you can do it in the follwing way.
It is necessary to generation your own python virtual environment, and to create the following environment variables:

% export FLASK_APP=chatbot.py
% export FLASK_DEBUG=1 
% flask run


## Unit tests 

Unit tests are placed in the tests directory and can be executed using the command:

% export FLASK_APP=chatbot.py

% export FLASK_DEBUG=1 

%  flask test 


## Installation and building blocks
It is used a modified library ChatterBot-spacy_fixed to avoid problems with the ChatterBot library which is not maintained since 2020:

git clone git@github.com:feignbird/ChatterBot-spacy_fixed.git
pip install ./ChatterBot-spacy_fixed
pip install chatterbot-corpus
pip uninstall pyYAML
pip install pyYAML==5.3.1
python -m spacy download en_core_web_sm

In order to enable context management of conversations the ChatterBot-spacy_fixed library is further modified and that's the reason why ChatterBot is installed from the ChatterBot-1.1.0a7.tar.gz file.
