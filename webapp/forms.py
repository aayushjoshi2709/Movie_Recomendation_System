from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
class recommendation_form(FlaskForm):
    movie_name = SelectField(label="Select a Movie", validators=[DataRequired()])
    submit = SubmitField(label='Recommend Movies')