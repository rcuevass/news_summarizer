from flask import Flask, render_template, request
from GoogleNews import GoogleNews
from newsapi import NewsApiClient
from utils.logging import get_log_object
import os
import requests
from forms import UrlSearchForm

# import nltk
# nltk.data.path.append('./nltk_data/')

from newspaper import Article
from wordcloud import WordCloud

import base64
import io
import datetime


app = Flask(__name__)
googlenews = GoogleNews()
# Init
newsapi_x = NewsApiClient(api_key='bbaf79e491bd41c486f9df1b455a0c62')

log = get_log_object()


@app.route('/', methods = ["GET", "POST"])
def index():
    errors = []
    urlsearch = UrlSearchForm(request.form)
    log.info('URL zero=%s', urlsearch)

    if request.method == "POST":
        
        try:
            return search_results(urlsearch)
        except:
            errors.append(
                "Unable to get the URL.  Please enter a valid URL for news article."
            )       
    return render_template("index.html", form = urlsearch, errors = errors)


def search_results(urlsearch):

    urlsearch = UrlSearchForm(request.form)

    search_string = urlsearch.data['search']

    #googlenews.search(search_string)
    #link_to_search = googlenews.get_links()[0]
    #googlenews.clear()

    log.info('search_string=%s', search_string)

    article = Article(search_string)
    log.info('Type article=%s', str(article))
    log.info('Article instantiated')

    article.download()
    log.info('Article downloaded')
    article.parse()
    log.info('Article parsed')
    # nltk.download("punkt")
    article.nlp()
    log.info('Article NLP-ed')

    data = article.text
    title = article.title
    date = article.publish_date
    published_date = date.strftime("%d %B %Y")
    author = article.authors[0]
    log.info('author=%s', author)
    image = article.top_image
    log.info('image=%s', str(image))

    # WordCloud disabled for now
    # cloud = get_wordcloud(data)
    keyword = article.keywords

    summary = article.summary

    return render_template("results.html", search_string = search_string, title = title, published_date=published_date,
                           author = author, image = image, keyword = keyword, summary = summary)


if __name__ == '__main__':
    app.run()
