from flask import Flask, render_template, request
from GoogleNews import GoogleNews
from newsapi import NewsApiClient
from utils.logging import get_log_object
from utils.get_credentials import get_api_news_credential

from newsapi import NewsApiClient
from datetime import date, timedelta

from forms import UrlSearchForm
import sys

# import nltk
# nltk.data.path.append('./nltk_data/')

from newspaper import Article

app = Flask(__name__)
googlenews = GoogleNews()
# Init
api_key_val = get_api_news_credential()
newsapi_x = NewsApiClient(api_key=api_key_val)
todays_date = date.today()
past_date = todays_date - timedelta(3)

log = get_log_object()

# https://www.bbc.com/news/technology-55044568


@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    urlsearch = UrlSearchForm(request.form)
    log.info('URL zero=%s', urlsearch.data['search'])

    if request.method == "POST":
        
        try:
            results_from_req = search_results(urlsearch)
            return results_from_req

        except:
            errors.append(
                "Unable to process request. This event has been logged and it will be tackled in next release"
            )
            log.info('It was not possible to process this URL=%s', urlsearch.data['search'])
    return render_template("index.html", form = urlsearch, errors = errors)


def search_results(input_):

    urlsearch_x = UrlSearchForm(request.form)
    search_string = urlsearch_x.data['search']
    log.info('String to be processed=%s', search_string)
    log.info('First four characters of the request=%s', search_string[:4])

    # initialize value for search_url
    search_url = None

    if search_string[:4] == 'http':
        log.info('URL detected')
        urlsearch_x = UrlSearchForm(request.form)
        search_url = urlsearch_x.data['search']
        log.info('URL to be processed=%s', search_url)

    else:
        try:
            all_articles = newsapi_x.get_everything(q=search_string,
                                                    sources='bbc-news,the-verge,abc-news,al-jazeera-english,'
                                                            'ars-technica, associated-press,axios,bloomberg,'
                                                            'business-insider,cbc-news,cnn,crypto-coins-news,'
                                                            'financial-post,google-news,google-news-ca,politico,'
                                                            'reuters,the-globe-and-mail,the-wall-street-journal,'
                                                            'the-washington-post,the-washington-times,wired',
                                                    domains='bbc.co.uk,theverge.com,bloomberg.com,nytimes.com,'
                                                            'bnnbloomberg.ca',
                                                    from_param=past_date,
                                                    to=todays_date,
                                                    language='en',
                                                    sort_by='popularity',
                                                    page=1)
            if len(all_articles['articles']) > 0:
                search_url = all_articles['articles'][0]['url']
                log.info('Query requested=%s', search_string)
                log.info('URL from NewsAPI=%s', search_url)
            else:
                log.info('Not relevant result were found from the query %s= ', search_string)

        except:
            log.info('It is likely you have made too many requests recently. Developer accounts are limited to 100')
            log.info('requests over a 24 hour period (50 requests available every 12 hours). Please upgrade to a paid')
            log.info('plan if you need more requests.')

    log.info('search URL=%s', search_url)

    article = Article(search_url)
    log.info('Type article=%s', str(article))
    log.info('Article instantiated')

    article.download()
    log.info('Article downloaded')
    article.parse()
    log.info('Article parsed')
    # nltk.download("punkt")
    article.nlp()
    log.info('Article NLP-ed')

    image = article.top_image
    log.info('image=%s', str(image))

    data = article.text
    log.info('Article data-ed')
    title = article.title
    log.info('Article title=%s', title)

    date = article.publish_date
    log.info('Article date=%s', bool(date))
    if not bool(date):
        published_date = 'Not specified'
        log.info('Published date was originally None - it has been replaced to Not Specified')
    else:
        published_date = date.strftime("%d %B %Y")

    log.info('Published date=%s', published_date)

    try:
        author = article.authors[0]
    except:
        author = 'Not specified'
    log.info('author=%s', author)

    keyword = article.keywords

    summary = article.summary

    return render_template("results.html", search_string = search_string, title = title, published_date=published_date,
                           author = author, image = image, keyword = keyword, summary = summary)


if __name__ == '__main__':
    app.run()
