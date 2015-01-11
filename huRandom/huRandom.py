from os import environ
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash


DATABASE = '/tmp/huRand.db'
DEBUG = True
SECRET_KEY = 'development key'


app = Flask(__name__)
app.config.from_object(__name__)

if __name__ == '__main__':
    app.run(host=environ.get('APP_IP'))
