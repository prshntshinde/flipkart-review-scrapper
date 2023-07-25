from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="logs/scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/review", methods=["GET","POST"])
def index():
    if request.method == "POST":
        return "OK"
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)