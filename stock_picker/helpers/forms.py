from flask_wtf import Form
from wtforms import  StringField, SelectField, DateField, SubmitField, BooleanField, TextField, PasswordField, validators
from wtforms.validators import DataRequired
from werkzeug import secure_filename
from flask.ext.uploads import UploadSet, IMAGES, TEXT
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import datetime, date

text = UploadSet('text', TEXT)

class PickForm(Form):
	textType = SelectField('Type', choices=[('book', 'BOOK'), ('poem', 'POEM'), ('lyric', 'LYRIC'), ('custom', 'CUSTOM')], validators=[DataRequired()])
	title = StringField('Title', validators=[DataRequired(), validators.Length(min = 1, max = 200)])
	author = StringField('Author', validators=[DataRequired(), validators.Length(min=4, max = 60)])
	description = StringField('Description')
	pub_date = DateField('Publication date')
	upload = FileField('Your text file', validators=[FileRequired(), FileAllowed(text, "Text only!")])
	submit = SubmitField("Submit")


class SearchForm(Form):
	search = StringField('Search by ticker or company name', validators = [DataRequired(), validators.Length(min = 1, max = 100)])
	submit = SubmitField("Submit")


class StockForm(Form):
	date_field  = DateField('See stock information for a given day (YYYY-MM-DD)', validators = [DataRequired()])