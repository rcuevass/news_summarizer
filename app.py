from flask import Flask, render_template, request
from GoogleNews import GoogleNews
from newsapi import NewsApiClient
from utils.logging import get_log_object
from utils.get_credentials import get_api_news_credential
from newspaper import Article
from datetime import date, timedelta
from forms import UrlSearchForm
import sys

# The following import is used the first time to extract data from NLTK and place it
# under the ./nltk_data folder.
# import nltk
# nltk.data.path.append('./nltk_data/')

# Instantiate the app with Flask
app = Flask(__name__)

# get token for APINews
api_key_val = get_api_news_credential()
newsapi_val = NewsApiClient(api_key=api_key_val)
# get todays's date and, from it, get the date corresponding to three days prior to it
todays_date = date.today()
past_date = todays_date - timedelta(1)

# instantiate logging object
log = get_log_object()


# set GET and POST methods for the app
@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    url_search = UrlSearchForm(request.form)
    log.info('URL to be processed=%s', url_search.data['search'])

    # to display results (POST)
    if request.method == "POST":
        
        try:
            results_from_req = search_results(url_search)
            log.info('Returning results of the request')
            return results_from_req

        except:
            errors.append(
                "Unable to process request. This event has been logged and it will be tackled in next release"
            )
            log.info('It was not possible to process this URL=%s', url_search.data['search'])
    return render_template("index.html", form = url_search, errors = errors)


def search_results(input_):

    url_search_news = UrlSearchForm(request.form)
    search_string = url_search_news.data['search']
    log.info('String to be processed=%s', search_string)
    log.info('First four characters of the request=%s', search_string[:4])

    # initialize value for search_url
    search_url = None

    # if string provided is candidate to be a URL...
    if search_string[:4] == 'http':
        log.info('Candidate to URL has be provided directly...')
        url_search_news = UrlSearchForm(request.form)
        search_url = url_search_news.data['search']
        log.info('URL to be processed=%s', search_url)

    else:
        log.info('An open string has been provided in the search bar...')
        try:
            all_articles = newsapi_val.get_everything(q=search_string,
                                                      sources='bbc-news, the-verge, abc-news, al-jazeera-english,'
                                                              'ars-technica, associated-press, axios,bloomberg,'
                                                              'business-insider, cbc-news, cnn, crypto-coins-news,'
                                                              'financial-post, google-news, google-news-ca, politico,'
                                                              'reuters, the-globe-and-mail, the-wall-street-journal,'
                                                              'the-washington-post, the-washington-times, wired',
                                                      domains='bbc.co.uk, theverge.com, bloomberg.com, nytimes.com,'
                                                              'bnnbloomberg.ca',
                                                      from_param=past_date,
                                                      to=todays_date,
                                                      language='en',
                                                      sort_by='popularity',
                                                      page=1)
            log.info('Articles have been obtained by means of newsAPI')

            # get total number of articles found
            tot_num_articles = len(all_articles['articles'])
            log.info('Total number of articles found=%i based on search=%s', tot_num_articles, search_string)
            # if at least one article was found...
            if tot_num_articles >= 1:
                search_url = all_articles['articles'][0]['url']
                log.info('Query requested=%s', search_string)
                log.info('URL from NewsAPI=%s', search_url)
                # replace search_url with search_string
                search_string = search_url

            else:
                log.info('Not relevant result were found from the query %s= ', search_string)

        except:
            log.info('It is likely you have made too many requests recently. Developer accounts are limited to 100')
            log.info('requests over a 24 hour period (50 requests available every 12 hours). Please upgrade to a paid')
            log.info('plan if you need more requests.')

    log.info('Final URL searched=%s', search_url)
    # instantiate Article object
    log.info('Instantiating Article object')
    article = Article(search_url)
    log.info('Article instantiated')

    article.download()
    log.info('Article downloaded')
    article.parse()
    log.info('Article parsed')
    # nltk.download("punkt")
    article.nlp()
    log.info('Article processed via NLP method')

    # getting URL to the image...
    image_url = article.top_image
    log.info('URL to image=%s', str(image_url))

    # in case text of article is needed
    # text_article = article.text

    # get title of article
    article_title = article.title
    log.info('Article title=%s', article_title)

    date_from_article_class = article.publish_date
    log.info('Date from Article class=%s', date_from_article_class)
    if not bool(date_from_article_class):
        published_date = 'Not specified'
        log.info('Published date was not originally specified in article - it has been replaced to Not Specified')
    else:
        published_date = date_from_article_class.strftime("%d %B %Y")

    log.info('Published date=%s', published_date)

    try:
        # get author from article if possible...
        author = article.authors[0]

    except:
        # otherwise change it to Not specified
        author = 'Not specified'

    log.info('Author of article=%s', author)

    # get article keywords and summary
    keywords = article.keywords
    log.info('Keywords gathered')
    log.info('Keywords found=%s', str(keywords))

    summary = article.summary
    log.info('Summary of article obtained...')

    # render results
    return render_template("results.html", search_string=search_string, title=article_title,
                           published_date=published_date, author=author, image=image_url, keyword=keywords,
                           summary=summary)


if __name__ == '__main__':
    app.run()
