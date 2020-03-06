from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, url
from wtforms.fields.html5 import URLField


class PaperForm(FlaskForm):
    citation = TextAreaField('Citation', validators=[DataRequired()])
    link = URLField('Link', validators=[url()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')
