from app import db
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orgm import mapper
from sqlalchemy.dialetcs.postgresql import JSON

class Stock(db.Model):
	query = db_sessio
	__tablename__ = 'stocks'
	ticker = db.Column(db.String(), primary_key = True)
	company_name = db.Column(db.String())
	index = db.Column(db.String())

class Stock(

	 
