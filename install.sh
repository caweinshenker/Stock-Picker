#Handle dependencies and add relevant packages to PYTHONPATh

echo Installing flask
pip install flask --user
echo Installing flask sqlalchemy
pip install flask-sqlalchemy --user
echo Installing yahoo_finance
pip install yahoo_finance --user
echo Installing autoenv
pip install autoenv --user
echo Installing wtforms
pip install wtforms --user
echo Installing Flask-WTF
pip install Flask-WTF --user
echo Installing Flask-Uploads
pip install Flask-Uploads --user
echo Installing wtforms_components
pip install wtforms_components --user
echo Augmenting PYTHONPATH to support installations
echo 'export PYTHONPATH="${PYTHONPATH}:~/.local/lib/python3.4/site-packages"' >> ~/.bashrc
