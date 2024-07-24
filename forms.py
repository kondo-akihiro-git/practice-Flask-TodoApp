from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class TodoForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    submit = SubmitField('Add Todo')
