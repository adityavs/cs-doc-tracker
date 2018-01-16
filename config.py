import os

password = os.environ['MYSQL_PASSWORD']

SQLALCHEMY_DATABASE_URI = 'mysql://root:' + password + '@localhost/bitsavers'
SQLALCHEMY_TRACK_MODIFICATIONS=True
