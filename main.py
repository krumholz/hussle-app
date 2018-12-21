from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''

@app.route("/")
def hello():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
