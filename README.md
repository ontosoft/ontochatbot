# Ontochatbot


## Running application
In order to start the application with generation of your virtual environment, it is necessary to create the following environment variables:

% export FLASK_APP=chatbot.py
% export FLASK_DEBUG=1 
% flask run


## Unit tests 

Unit tests are placed in the tests directory and can be executed using the command:

% export FLASK_APP=chatbot.py
% export FLASK_DEBUG=1 

%  flask test 


## Installation and building blocks
It is used ChatterBot-spacy_fixed to avoid problems with the ChatterBot library which is not maintained since 2020:

git clone git@github.com:feignbird/ChatterBot-spacy_fixed.git
pip install ./ChatterBot-spacy_fixed
pip install chatterbot-corpus
pip uninstall pyYAML
pip install pyYAML==5.3.1
python -m spacy download en_core_web_sm

