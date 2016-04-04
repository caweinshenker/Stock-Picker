#all the imports
from flask import Flask, request, session, g, redirect, url_for, \ 
	abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

#configuration
app = Flask(__name__)
DEBUG = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/caweinsh_
