from flask_wtf import Form
from wtforms import  StringField, SelectField, DateField, SubmitField, BooleanField, TextField, PasswordField, validators
from wtforms.validators import DataRequired
from werkzeug import secure_filename
from flask.ext.uploads import UploadSet, IMAGES, TEXT
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PickForm(Form):
	text = UploadSet('text', TEXT)
	textType = SelectField('Type', choices=[('book', 'BOOK'), ('poem', 'POEM'), ('lyric', 'LYRIC'), ('custom', 'CUSTOM')], validators=[DataRequired()])
	author = TextField('Author', validators=[DataRequired(), validators.Length(min=4, max = 60)])
	pub_date = DateField('Publication date')
	album = TextField('Album', validators=[validators.Length(min=2, max = 100)]) 
	upload = FileField('Your text file', validators=[FileRequired(), FileAllowed(text, "Text only!")])
	submit = SubmitField("Submit")
