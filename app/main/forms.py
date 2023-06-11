from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#This form is not used in this version
class HelloForm(FlaskForm):
    name = StringField('', 
        render_kw={'class': 'text-box', 'contenteditable':'true', 'disabled':'true'})
    submit = SubmitField('Send', 
        render_kw={'id': 'sendMessage'})
