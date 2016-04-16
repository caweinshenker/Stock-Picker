from flask_wtf import Form
from wtforms import  StringField, SelectField, DateField, SubmitField, BooleanField, TextField, IntegerField, validators
from wtforms_components import DateTimeField, DateRange
from wtforms.validators import DataRequired
from werkzeug import secure_filename
from werkzeug.datastructures import MultiDict
from flask.ext.uploads import UploadSet, IMAGES, TEXT
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import datetime, date, timedelta
from database import Db

text = UploadSet('text', TEXT)


class SearchForm(Form):
	search = StringField('Search by ticker or company name', validators = [DataRequired(), validators.Length(min = 1, max = 100)])
	submit = SubmitField("Submit")


class UploadForm(Form):
	textType = SelectField('Type', choices = [('book', 'Book'), ('poem', 'Poem'), ('lyric', 'Lyric'), ('custom', 'Custom')], validators = [DataRequired()])
	title = StringField('Title', validators =[DataRequired(), validators.Length(min= 1, max = 200)])
	author = StringField('Author', validators = [DataRequired(), validators.Length(min = 4, max = 60)])
	description = StringField('Description')
	pub_date = DateField('Publication date')
	upload = FileField('Your text file', validators = [FileRequired(), FileAllowed(text, "Text only!")])
	submit = SubmitField("Submit")


class StockForm(Form):
	date_field  = DateTimeField('See stock information for a given day (YYYY-MM-DD)', format = "%Y-%m-%d", validators = [DataRequired(), DateRange( min = datetime(2006, 04, 04), max = datetime(2016, 04, 04))])
	submit = SubmitField("Submit")

class PickForm(Form):
	database = Db()
	database.execute("SELECT file_location, title FROM text;", None)
	cur = database.get_cur()
	entries = [(row[0], row[1]) for row in cur.fetchall()]
	text = SelectField('Text', choices = entries, validators = [DataRequired()])
	money = IntegerField('Investment', validators = [DataRequired(), validators.NumberRange(min=1, max=100000000)])
	start_date = DateTimeField('Start date', format = "%Y-%m-%d", validators = [DataRequired(), DateRange( min = datetime(2006, 04, 04), max = datetime(2016, 04, 04))])
	end_date = DateTimeField('End date', format = "%Y-%m-%d", validators = [DataRequired(), DateRange( min = datetime(2006, 04, 04) , max = datetime(2016, 04, 04))])
	submit = SubmitField("Go!")
		

 
	
	
