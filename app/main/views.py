from flask import (Flask, render_template, session, redirect, url_for,  
    flash, request, jsonify)
from .forms import HelloForm
from . import main
from ..ontochat import chatbot 
from flask import current_app

@main.route('/', methods = ['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        chat_name = session.get('name')
        if chat_name is not None and chat_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('main.index'))
    return render_template('index.html', 
        form = form, name = session.get('name'))

@main.route("/chatresponse", methods=['POST'])
def process_chatbot_response():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        input_message = request.json.get('message')
        current_app.logger.debug("Chat - input message:" + input_message)
        response1 = chatbot.get_response(input_message)
        current_app.logger.debug("Chat - response1: " + response1.text)
        # if some other LogicAdapter responds to the input message then the system
        # asks whether the user wants to continue with the job of the OntoChatterAdapter  
        list_of_responces = [{'response': response1.text}]
        current_app.logger.debug("Current adapter: "  + response1.created_by_adapter)
        if response1.created_by_adapter != 'OntoChatterAdapter':
            current_app.logger.debug("Chat - input message: " + "")
            response2 = chatbot.get_response("")
            current_app.logger.debug("Chat - response2: " + response2.text)
            current_app.logger.debug("Chat - Adapter: " + str(response2.created_by_adapter))
            list_of_responces.append ({'response': response2.text})
        return jsonify(list_of_responces)
    else:
        return 'Content-Type not supported!'
