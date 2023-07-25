from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="logs/scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def test():
    return "OK"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)