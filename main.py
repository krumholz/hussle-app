import os

from flask import Flask, render_template, jsonify
import sqlalchemy

import twitter

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

api = twitter.Api(consumer_key = os.environ.get('TWITTER_KEY'),
    consumer_secret = os.environ.get('TWITTER_SECRET'),
    access_token_key = os.environ.get('TWITTER_ACCESS_KEY'),
    access_token_secret = os.environ.get('TWITTER_TOKEN_SECRET'),
    tweet_mode='extended')

# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`
if os.environ.get('GAE_ENV') == 'standard':
    # If deployed, use the local socket interface for accessing Cloud SQL
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    engine_url = 'mysql+pymysql://{}:{}@/{}?unix_socket={}'.format(
        db_user, db_password, db_name, unix_socket)
else:
    # If running locally, use the TCP connections instead
    # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
    # so that your application can use 127.0.0.1:3306 to connect to your
    # Cloud SQL instance
    host = '127.0.0.1'
    engine_url = 'mysql+pymysql://{}:{}@{}/{}'.format(
        db_user, db_password, host, db_name)

# The Engine object returned by create_engine() has a QueuePool integrated
# See https://docs.sqlalchemy.org/en/latest/core/pooling.html for more
# information
engine = sqlalchemy.create_engine(engine_url, pool_size=3)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("layout.html")

@app.route('/db')
def db():
    cnx = engine.connect()
    cursor = cnx.execute('SELECT * from innodb_buffer_stats_by_schema;')
    results = cursor.fetchall()
    a = []
    for row in results:
        a.append(str(row))
    cnx.close()

    return jsonify(a)

    # return str(current_time)

@app.route('/twitter')
def twitter():
    timeline = api.GetHomeTimeline()
    a = []
    for tweet in timeline:
        return jsonify(tweet._json)
    # for tweet in timeline:
    #     return tweet


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
