from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class LectureForm(FlaskForm):
    question_query = StringField('Press Enter to clear.', validators=[DataRequired(), Length(max=25)],
                                 id='search-bar')
