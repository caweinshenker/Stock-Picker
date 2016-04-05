TASKS IN DECREASING ORDER OF IMPORTANCE -- WITH DEADLINES
=========================================================



1. Postgres connection
	
	DELIVERABLES:
		1. Modified Stock-picker/app.py

	PROBLEM:
		We should be able to setup an @app.beforerequest and @app.teardownrequest in app.py so that a database connection is opened and closed with each route.
		I have not been able to figure out how to make this happen with postgres on flask. Flask does not natively support PG, but the Flask-SQLAlchemy extension
		is the preferred method of handling this. Figure out how to make SQLalchemy open a connection to the stock-picker database.

	SOLUTIONS:
		Read the docs.

	DOCS:
		http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#sql-abstraction-layer
		http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html
		http://flask-sqlalchemy.pocoo.org/2.1/api/
		http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/declarative/api.html
		http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/
		http://docs.sqlalchemy.org/en/latest/core/engines.html			

	
	DEADLINE: 4/10/2016




2. HTML/Jinja2 template for viewing a list of all the stocks in the database

	DELIVERABLES:
		1. stock-picker/templates/browse.html
		2. stock-picker/static/css.browse.css
		3. stock-picker/static/js/browse.js
		4. Updates app.py file to reflect new route	
	
	DOCS:
		http://flask.pocoo.org/docs/0.10/tutorial/templates/#layout-html
		
	DEADLINE:
		4/10/2016



3. HTML/Jinja2 template for an HTML form that lets users upload a text file for parsing or choose a file from the database

	DELIVERABLES:
		1. stock-picker/templates/pick.html
		2. stock-picker/static/css/pick.css
		3. stock-picker/static/js/pick.js
	        4. Updated app.py file to reflect new route
	DOCS:
		http://flask.pocoo.org/docs/0.10/patterns/wtforms/

	DEADLINE: 4/11/2016
	



4. HTML/Jinja 2 template for viewing the results of the text parsing algorithm
	
	DELIVERABLES:
		1.stock-picker/templates/results.html
		2.stock-picker/static/css/results.css
		3.stock-picker/static/js/results.js
		4.Updated app.py file to reflect new route


	DEADLINE:
		4/12/2016



5.HTML/Jinja 2 templates for site header/footer

	DELIVERABLES:
		1.stock-picker/templates/header.html
		2.stock-picker/static/css/header.css
		3.stock-picker/static/js/header.js
		4.stock-picker/templates/footer.html
		5.stock-picker/static/css/footer.css
		6.stock-picker/static/js/footer.js
	 	


	DEADLINE:
		4/13/2016


6. Setup.py

	DELIVERABLES:
		1. Convert the config/install.sh file into a python script setup.py that sits in the main directory of the flask app
		2. Remove config directory


	DOCS:
		none
	
	DEADLINE:
		4/16/2016



