import logging.config
import os
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import settings
import requests
import json
from feedgen.feed import FeedGenerator
from flask import make_response
from urllib.parse import urljoin
from werkzeug.contrib.atom import AtomFeed
from os import environ

app = Flask(__name__)
Bootstrap(app)



def get_abs_url(url):
    """ Returns absolute url by joining post url with base url """
    return urljoin(request.url_root, url)


@app.route('/')
def home():
    response = [{
        "title" : "Ad Title",
        "description" : "Ad Description"
    }]
    response2 = [{
        "title" : "Ad Title",
        "description" : "Ad Description"
    }]

    ads = response.json()
    posts = response2.json()
    return render_template("index.html", ads=ads, posts=posts)


@app.route('/ad/add', methods=['GET'])
def add_ad_view():
    return render_template("new_ad.html")


@app.route('/ad/edit/<id>', methods=['GET'])
def edit_ad_view(id):
    response = requests.get(settings.API_URL + '/getAdvertisement?id=' + id)
    ad = response.json()
    return render_template("edit_ad.html", ad=ad)


@app.route('/ad/delete/<id>', methods=['GET'])
def delete_ad_view(id):
    response = requests.get(settings.API_URL + '/getAdvertisement?id=' + id)
    ad = response.json()
    return render_template("delete_ad.html", ad=ad)

@app.route('/ad/view/<id>', methods=['GET'])
def view_ad_view(id):
    response = requests.get(settings.API_URL + '/getAdvertisement?id=' + id)
    ad = response.json()
    return render_template("view_ad.html", ad=ad)

@app.route('/ad/new', methods=['POST'])
def add_ad_request():
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }
    response = requests.post(settings.API_URL + '/createAdvertisement', json=json.dumps(req_data))
    return redirect(url_for('home'))

@app.route('/ad/update/<id>', methods=['POST'])
def update_ad_request(id):
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }
    response = requests.put(settings.API_URL + '/updateAdvertisement?id=' + id, json=json.dumps(req_data))
    return redirect(url_for('home'))

@app.route('/ad/delete/<id>', methods=['POST'])
def delete_ad_request(id):
    response = requests.delete(settings.API_URL + '/deleteAdvertisement?id=' + id)
    if response.status_code == 200:
        return redirect(url_for('home'))

# running app
def main():
    print(' ----->>>> Flask Python Application running in development server')
    HOST = environ.get('SERVER_HOST', 'localhost')
    PORT = int(environ.get('SERVER_PORT', '5555'))
    app.run(HOST, PORT, debug=settings.FLASK_DEBUG)


if __name__ == '__main__':
    main()
