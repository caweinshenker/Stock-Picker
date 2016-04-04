from app import db
from sqlalchemy.dialetcs.postgresql import JSON

class Stock(db.Model):
	__tablename__ = 'stocks'
	ticker = db.Column(db.String(), primary_key = True)
	company_name = db.Column(db.String())
	 
