import logging
from urllib.request import urlopen as uReq

import pymongo
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin

logging.basicConfig(filename="logs/scrapper.log", level=logging.INFO)

app = Flask(__name__)


@app.route("/", methods=["GET"])
@cross_origin
def homepage():
    return render_template("index.html")


@app.route("/review", methods=["GET", "POST"])
@cross_origin
def index():
    if request.method == "POST":
        try:
            search_string = request.form['keyword'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            url_client = uReq(flipkart_url)
            flipkart_page = url_client.read()
            url_client.close()
            flipkart_html = bs(flipkart_page, "html.parser")
            # print(flipkart_html)
            results_container = flipkart_html.find_all(
                "div", {"class": "_1AtVbE col-12-12"})
            # print(results_container)
            del results_container[0:3]
            result = results_container[0]
            product_link = "https://www.flipkart.com" + \
                result.div.div.div.a['href']
            print(product_link)
            product_result = requests.get(product_link)
            product_result.encoding = "utf-8"
            product_html = bs(product_result.text, "html.parser")
            # print(product_html)
            comment_container = product_html.find_all(
                "div", {"class": "_16PBlm"})

            filename = search_string + ".csv"
            with open(filename, "w") as fw:
                headers = "Product, Customer Name, Rating, Heading, Comment \n"
                fw.write(headers)
            reviews = []

            for commentbox in comment_container:
                try:
                    name = commentbox.div.div.find_all(
                        'p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    logging.info("name")

                try:
                    # rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'
                    logging.info("rating")

                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)
                try:
                    comtag = commentbox.div.div.find_all(
                        'div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    logging.info(e)

                mydict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            logging.info("log my final result {}".format(reviews))

            # MongoDB integration
            client = pymongo.MongoClient(
                "mongodb+srv://prashant:Z6BBqU53PIU60BRM@skills-cluster.mzqp9kr.mongodb.net/?retryWrites=true&w=majority")
            db = client['flipkart-scrapper']
            collection = db['records']
            collection.insert_many(reviews)

            return render_template("result.html", reviews=reviews[0:(len(reviews) - 1)])

        except Exception as e:
            logging.info(e)
            return "Something is wrong. "
        """ finally:
            return render_template("index.html") """
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
